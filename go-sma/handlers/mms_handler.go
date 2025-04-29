package handlers

import (
	"database/sql"
	"encoding/json"
	"errors"
	"fmt"
	"log"
	"net/http"
	"strconv"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/jeanmamelo/go-sma/models"
)

func MMSHandler(db *sql.DB) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		log.Println("new request received")
		pair := chi.URLParam(r, "pair")
		if pair != "BRLBTC" && pair != "BRLETH" {
			http.Error(w, "invalid pair", http.StatusBadRequest)
			return
		}

		var pairMapping = map[string]string{
			"BRLBTC": "BTC-BRL",
			"BRLETH": "ETH-BRL",
		}

		mappedPair, ok := pairMapping[pair]
		if !ok {
			http.Error(w, "invalid pair", http.StatusBadRequest)
			return
		}

		fromStr := r.URL.Query().Get("from")
		toStr := r.URL.Query().Get("to")
		rangeStr := r.URL.Query().Get("range")

		log.Printf("pair: %s, from: %s, to: %s, range: %s\n", pair, fromStr, toStr, rangeStr)

		if fromStr == "" {
			http.Error(w, "missing 'from' param", http.StatusBadRequest)
			return
		}

		fromInt, err := strconv.ParseInt(fromStr, 10, 64)
		if err != nil {
			http.Error(w, "invalid 'from' timestamp", http.StatusBadRequest)
			return
		}
		from := time.Unix(fromInt, 0)

		var to time.Time
		if toStr == "" {
			to = time.Now().AddDate(0, 0, -1)
		} else {
			toInt, err := strconv.ParseInt(toStr, 10, 64)
			if err != nil {
				http.Error(w, "invalid 'to' timestamp", http.StatusBadRequest)
				return
			}
			to = time.Unix(toInt, 0)
		}

		window, err := strconv.Atoi(rangeStr)
		if err != nil || (window != 20 && window != 50 && window != 200) {
			http.Error(w, "invalid 'range' param (must be 20, 50 or 200)", http.StatusBadRequest)
			return
		}

		if !validateFromDate(from) {
			log.Println("error to fetch candles: 'from' cannot be older than 365 days", from)
			http.Error(w, "start date cannot be older than 365 days", http.StatusBadRequest)
			return
		}

		candles, err := fetchCandles(db, mappedPair, from, to, window)
		if err != nil {
			if errors.Is(err, sql.ErrNoRows) || err.Error() == "no candles found" {
				http.Error(w, "no candles found", http.StatusNotFound)
				return
			}
			http.Error(w, "error fetching candles: "+err.Error(), http.StatusInternalServerError)
			return
		}

		log.Println("successfully fetched candles")

		w.Header().Set("Content-Type", "application/json")
		w.WriteHeader(http.StatusOK)
		json.NewEncoder(w).Encode(candles)
	}
}

func validateFromDate(from time.Time) bool {
	oneYearAgo := time.Now().AddDate(-1, 0, 0)
	return from.After(oneYearAgo) || from.Equal(oneYearAgo)
}

func fetchCandles(db *sql.DB, pair string, from, to time.Time, window int) ([]models.Candle, error) {
	mmsField := map[int]string{
		20:  "mms_20",
		50:  "mms_50",
		200: "mms_200",
	}[window]

	query := fmt.Sprintf(`
        SELECT timestamp, %s
        FROM pair
        WHERE pair = $1 AND timestamp BETWEEN $2 AND $3
        ORDER BY timestamp ASC
    `, mmsField)

	rows, err := db.Query(query, pair, from, to)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var candles []models.Candle
	for rows.Next() {
		var (
			timestamp time.Time
			mms       sql.NullFloat64
		)
		if err := rows.Scan(&timestamp, &mms); err != nil {
			return nil, err
		}

		candle := models.Candle{
			Timestamp: timestamp,
		}
		if mms.Valid {
			candle.Mms = &mms.Float64
		}

		candles = append(candles, candle)
	}
	if len(candles) == 0 {
		return nil, errors.New("no candles found")
	}

	return candles, nil
}
