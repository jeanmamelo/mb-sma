package main

import (
	"log"
	"net/http"

	"github.com/go-chi/chi/v5"
	"github.com/jeanmamelo/go-sma/engines"
	"github.com/jeanmamelo/go-sma/handlers"
)

func main() {
	db, err := engines.Connect()
	if err != nil {
		log.Fatalf("Database connection error: %v", err)
	}
	defer db.Close()

	r := chi.NewRouter()

	r.Get("/{pair}/mms", handlers.MMSHandler(db))

	log.Println("Starting server on :8080...")
	http.ListenAndServe(":8080", r)
}
