package models

type Blog struct {
	ID      int    `json:"blog_id"`
	Title   string `json:"blog_title"`
	Content string `json:"blog_content"`
}
