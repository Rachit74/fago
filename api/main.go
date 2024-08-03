package main

import (
	"fago_api/db"
	"fago_api/handlers" // Import your handlers package here
	"log"
	"net/http"

	"github.com/gorilla/mux"
	// "github.com/rs/cors"
)

func main() {
	// Initialize the database
	db.InitDB()

	// Create a new router
	r := mux.NewRouter()

	// Register routes with the router
	handlers.RegisterRoutes(r)

	// // Set up CORS handling
	// c := cors.New(cors.Options{
	// 	AllowedOrigins: []string{"http://127.0.0.1:5000"}, // Replace with your Flask app's origin
	// 	AllowedMethods: []string{"GET", "POST", "DELETE", "OPTIONS"},
	// 	AllowedHeaders: []string{"Content-Type"},
	// })

	// // Wrap the router with CORS middleware
	// handler := c.Handler(r)

	// Start the HTTP server
	log.Fatal(http.ListenAndServe(":8080", r))
}
