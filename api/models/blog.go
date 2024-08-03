package models

import (
	"gorm.io/gorm"
)

type Blog struct {
	gorm.Model // ID, CreatedAt, UpdatedAt is in gorm by default
	Title      string
	Content    string
}
