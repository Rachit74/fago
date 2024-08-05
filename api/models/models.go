package models

import "gorm.io/gorm"

type User struct {
	gorm.Model
	Username string
	Email    string `gorm:"uniqueIndex"`
	Password string
	Blogs    []Blog `gorm:"foreignKey:UserID"`
}

type Blog struct {
	gorm.Model
	Title   string
	Content string
	UserID  uint
}
