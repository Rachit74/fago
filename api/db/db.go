package db

import (
	"fago_api/models"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

func InitDB() {
	db, err := gorm.Open(sqlite.Open("database.db"), &gorm.Config{})
	if err != nil {
		panic("Failed to open db")
	}

	err = db.AutoMigrate(&models.Blog{})
	if err != nil {
		panic("Failed to Migrage")
	}

}

func CreateBlog(blog *models.Blog) error {
	result := DB.Create(blog)
	return result.Error
}

func GetBlog(id uint) (*models.Blog, error) {
	var blog models.Blog
	result := DB.First(&blog, id)
	if result.Error != nil {
		return nil, result.Error
	}
	return &blog, nil
}

func GetBlogs() ([]models.Blog, error) {
	// declares an empty slice which will hold the values from the database
	var blogs []models.Blog
	result := DB.Find(&blogs)
	if result.Error != nil {
		return nil, result.Error
	}
	return blogs, nil
}

func DeleteBlog(id uint) error {
	result := DB.Delete(&models.Blog{}, id)
	return result.Error
}
