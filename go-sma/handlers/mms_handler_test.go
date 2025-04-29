package handlers_test

import (
	"net/http"
	"net/http/httptest"
	"testing"

	"github.com/DATA-DOG/go-sqlmock"
	"github.com/jeanmamelo/go-sma/handlers"
	"github.com/stretchr/testify/assert"
)

func TestMMSHandler_InvalidPair(t *testing.T) {
	db, _, _ := sqlmock.New()
	defer db.Close()

	req := httptest.NewRequest(http.MethodGet, "/INVALID/mms?from=1690000000&range=20", nil)
	rr := httptest.NewRecorder()

	handler := handlers.MMSHandler(db)
	handler.ServeHTTP(rr, req)

	assert.Equal(t, http.StatusBadRequest, rr.Code)
	assert.Contains(t, rr.Body.String(), "invalid pair")
}
