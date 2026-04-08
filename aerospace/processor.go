package aerospace

import (
	"context"
	"errors"
	"fmt"
	"log"
	"time"
)

type PayoutStatus string

const (
	StatusPending PayoutStatus = "PENDING"
	StatusSuccess PayoutStatus = "SUCCESS"
	StatusFailed  PayoutStatus = "FAILED"
)

var ErrDuplicateIdempotencyKey = errors.New("duplicate idempotency key")

type Payout struct {
	ID            string
	Amount        float64
	Currency      string
	RecipientID   string
	Status        PayoutStatus
	IdempotencyID string
	CreatedAt     time.Time
}

type PaymentGateway interface {
	Transfer(ctx context.Context, p Payout) error
	CheckStatus(ctx context.Context, payoutID string) (PayoutStatus, error)
}

type Repository interface {
	SavePayout(ctx context.Context, p Payout) error
	UpdateStatus(ctx context.Context, id string, status PayoutStatus) error
	GetPendingPayouts(ctx context.Context, olderThan time.Duration) ([]Payout, error)
}

type PayoutProcessor struct {
	repo    Repository
	gateway PaymentGateway
}

func NewProcessor(r Repository, g PaymentGateway) *PayoutProcessor {
	return &PayoutProcessor{repo: r, gateway: g}
}

func (s *PayoutProcessor) ProcessPayout(ctx context.Context, p Payout) error {
	if p.Amount <= 0 {
		return errors.New("invalid amount: must be greater than zero")
	}

	p.Status = StatusPending
	p.CreatedAt = time.Now()

	if err := s.repo.SavePayout(ctx, p); err != nil {
		if errors.Is(err, ErrDuplicateIdempotencyKey) {
			return fmt.Errorf("payout already initiated for key: %s", p.IdempotencyID)
		}
		return fmt.Errorf("failed to initialize payout: %w", err)
	}

	err := s.gateway.Transfer(ctx, p)
	if err != nil {
		if dbErr := s.repo.UpdateStatus(ctx, p.ID, StatusFailed); dbErr != nil {
			log.Printf("[CRITICAL] Gateway AND DB update failed for Payout %s: %v", p.ID, dbErr)
		}
		return fmt.Errorf("gateway transfer failed: %w", err)
	}

	return s.repo.UpdateStatus(ctx, p.ID, StatusSuccess)
}

func (s *PayoutProcessor) StartReconciliationSweeper(ctx context.Context, interval time.Duration) {
	ticker := time.NewTicker(interval)
	go func() {
		for {
			select {
			case <-ctx.Done():
				log.Println("[AEROSPACE] Sweeper shutting down.")
				return
			case <-ticker.C:
				s.sweepGhostTransactions(ctx)
			}
		}
	}()
}

func (s *PayoutProcessor) sweepGhostTransactions(ctx context.Context) {
	stuckPayouts, err := s.repo.GetPendingPayouts(ctx, 10*time.Minute)
	if err != nil {
		log.Printf("[ERROR] Sweeper failed to query DB: %v", err)
		return
	}

	for _, p := range stuckPayouts {
		log.Printf("[SWEEPER] Investigating stuck payout: %s", p.ID)

		actualStatus, err := s.gateway.CheckStatus(ctx, p.ID)
		if err != nil {
			continue
		}

		if actualStatus != StatusPending {
			s.repo.UpdateStatus(ctx, p.ID, actualStatus)
			log.Printf("[SWEEPER] Reconciled Payout %s -> %s", p.ID, actualStatus)
		}
	}
}
