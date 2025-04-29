package models

import "time"

type Candle struct {
	Timestamp time.Time `json:"timestamp"`
	Mms       *float64  `json:"mms",omitempty`
}
