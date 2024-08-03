package main

import (
	"fago_api/db"
	"fago_api/handlers" // Import your handlers package here
	"log"
	"net/http"

	"github.com/gorilla/mux"
)

func main() {
	// Initialize the database
	db.InitDB()

	// Create a new router
	r := mux.NewRouter()

	// Register routes with the router
	handlers.RegisterRoutes(r)

	// Start the HTTP server
	log.Fatal(http.ListenAndServe(":8080", r))
}
