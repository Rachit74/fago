package handlers

import (
	"encoding/json"
	"fago_api/db"
	"fago_api/models"
	"net/http"
	"strconv"

	"github.com/gorilla/mux"
)

func CreateBlogHandler(w http.ResponseWriter, r *http.Request) {
	var blog models.Blog
	err := json.NewDecoder(r.Body).Decode(&blog)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
		return
	}

	err = db.CreateBlog(&blog)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	w.WriteHeader(http.StatusCreated)
	json.NewEncoder(w).Encode(blog)
}

// returns one particular blog
func GetBlogHandler(w http.ResponseWriter, r *http.Request) {
	// mux.vars extracts routes variables from the http request
	// vars is a map where key are the names of route variables and values are the values accosiated to the key variables
	vars := mux.Vars(r)
	// vars[id] gets the value of the root named id from the vars map
	// this converts a string into a unit
	id, err := strconv.ParseUint(vars["id"], 10, 32)
	if err != nil {
		http.Error(w, err.Error(), http.StatusBadRequest)
	}

	blog, err := db.GetBlog(uint(id))
	if err != nil {
		http.Error(w, err.Error(), http.StatusNotFound)
		return
	}
	json.NewEncoder(w).Encode(blog)
}

// returns all the blogs
func GetBlogsHandler(w http.ResponseWriter, r *http.Request) {
	blogs, err := db.GetBlogs()
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	json.NewEncoder(w).Encode(blogs)
}

func DeleteBlogHandler(w http.ResponseWriter, r *http.Request) {
	vars := mux.Vars(r)
	id, err := strconv.ParseUint(vars["id"], 10, 32)
	if err != nil {
		http.Error(w, "Invalid ID", http.StatusBadRequest)
		return
	}

	err = db.DeleteBlog(uint(id))
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	w.WriteHeader(http.StatusNoContent)
}

// RegisterRoutes sets up the routes for blog operations
func RegisterRoutes(r *mux.Router) {
	r.HandleFunc("/blogs", CreateBlogHandler).Methods("POST")
	r.HandleFunc("/blogs/{id:[0-9]+}", GetBlogHandler).Methods("GET")
	r.HandleFunc("/blogs", GetBlogsHandler).Methods("GET")
	r.HandleFunc("/blogs/{id:[0-9]+}", DeleteBlogHandler).Methods("DELETE")
}
