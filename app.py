import os
import json
import re
import requests
import time
from bs4 import BeautifulSoup
from flask import Flask, request, jsonify
from langchain.document_loaders import WebBaseLoader
from langchain_huggingface import HuggingFaceEmbeddings  # Updated import
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter  # Removed TokenTextSplitter import
from langchain.llms import HuggingFacePipeline
from langchain.chains import create_retrieval_chain  # Updated import
from langchain_core.prompts import PromptTemplate
from langchain.chains.combine_documents import create_stuff_documents_chain  # Import required function
from transformers import AutoTokenizer  # Import Hugging Face tokenizer

# Initialize Flask app
app = Flask(__name__)

# Define constants
DATA_URL = "https://brainlox.com/courses/category/technical"
EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
VECTOR_STORE_PATH = "faiss_index"
CACHE_DURATION = 1800  # Cache duration in seconds (30 minutes)
last_scraped_time = 0
cached_courses = []
cached_prices = {}

# Load tokenizer for FLAN-T5
tokenizer = AutoTokenizer.from_pretrained("google/flan-t5-large")

# Scrape course names and prices from Brainlox website
def load_data():
    """Scrape course names and prices from Brainlox website with caching."""
    global last_scraped_time, cached_courses, cached_prices
    current_time = time.time()

    if current_time - last_scraped_time < CACHE_DURATION and cached_courses:
        return cached_courses, cached_prices

    url = "https://brainlox.com/courses/category/technical"
    headers = {"User-Agent": "Mozilla/5.0"}  # Prevent getting blocked

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        courses = []
        prices = {}

        # Extract course names and prices
        for course_box in soup.select(".single-courses-box"):
            course_name_elem = course_box.select_one("h3 a")
            price_elem = course_box.select_one(".price .price-per-session")

            if course_name_elem:
                course_name = course_name_elem.get_text(strip=True)
                courses.append(course_name)
                
                if price_elem:
                    price = price_elem.get_text(strip=True)
                    prices[course_name] = price

        # Update cache
        last_scraped_time = current_time
        cached_courses = courses
        cached_prices = prices

        return courses, prices

    except requests.exceptions.RequestException as e:
        return [], {}

def categorize_courses(course_list):
    """Group courses into categories based on keywords."""
    categories = {
        "Python": [],
        "Java": [],
        "Web Development": [],
        "AI & Machine Learning": [],
        "Roblox & Game Dev": [],
        "Cloud Computing": [],
        "Scratch": [],
        "Others": []
    }

    for course in course_list:
        lower_course = course.lower()
        if "python" in lower_course:
            categories["Python"].append(course)
        elif re.search(r"\bjava\b", lower_course) and "javascript" not in lower_course:
            categories["Java"].append(course)
        elif re.search(r"\b(web development|html|css|javascript)\b", lower_course):
            categories["Web Development"].append(course)
        elif re.search(r"\b(ai|artificial intelligence|machine learning)\b", lower_course):
            categories["AI & Machine Learning"].append(course)
        elif re.search(r"\b(roblox|game)\b", lower_course):
            categories["Roblox & Game Dev"].append(course)
        elif re.search(r"\b(cloud|aws)\b", lower_course):
            categories["Cloud Computing"].append(course)
        elif "scratch" in lower_course:
            categories["Scratch"].append(course)
        else:
            categories["Others"].append(course)

    return categories

@app.route("/query", methods=["POST"])
def query():
    data = request.json
    user_query = data.get("query", "").strip().lower()

    if not user_query:
        return jsonify({"error": "Query is required"}), 400

    try:
        # Fetch real course names and prices
        scraped_courses, scraped_prices = load_data()

        if not scraped_courses:
            return jsonify({"response": "No courses found on Brainlox at the moment."})

        # Categorize courses
        categorized_courses = categorize_courses(scraped_courses)
        print("🔹 User Query:", user_query)

        # Check if the query asks for pricing information
        price_query = ("cost" in user_query or "price" in user_query)

        # Check for specific category requests and accumulate matches
        matching_categories = {}
        for category, courses in categorized_courses.items():
            if re.search(rf"\b{category.lower()}\b", user_query):
                matching_categories[category] = courses

        # If a specific category is requested and pricing is requested,
        # filter prices for only the courses in the matching category(ies)
        if matching_categories and price_query:
            filtered_prices = {}
            for category, courses in matching_categories.items():
                for course in courses:
                    if course in scraped_prices:
                        filtered_prices[course] = scraped_prices[course]
            return jsonify({"response": filtered_prices})

        # If only a specific category is requested without pricing
        if matching_categories:
            return jsonify({"response": matching_categories})

        # If only pricing is requested (no specific category), return all prices
        if price_query:
            return jsonify({"response": scraped_prices})

        # Generic query for listing available courses
        if "available" in user_query or "list" in user_query or "brainlox courses" in user_query:
            return jsonify({"response": categorized_courses})

        response = {"message": "I couldn't understand your query. Please ask about available courses, pricing, or a specific category like 'Java'."}
        print("🔹 No matching category found")

    except Exception as e:
        return jsonify({"response": "Error occurred during retrieval. Try again."})

    return jsonify({"response": response})



if __name__ == "__main__":
    app.run(debug=True)