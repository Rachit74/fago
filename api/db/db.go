package db

import (
	"errors"
	"fago_api/models"

	"gorm.io/driver/sqlite"
	"gorm.io/gorm"
)

var DB *gorm.DB

// InitDB initializes the database connection and performs auto-migration
func InitDB() {
	var err error
	DB, err = gorm.Open(sqlite.Open("database.db"), &gorm.Config{})
	if err != nil {
		panic("Failed to open db: " + err.Error())
	}

	err = DB.AutoMigrate(&models.Blog{})
	if err != nil {
		panic("Failed to migrate database: " + err.Error())
	}
	err = DB.AutoMigrate(&models.User{})
	if err != nil {
		panic("Failed to migrate database: " + err.Error())
	}
}

// CreateBlog creates a new blog entry in the database
func CreateBlog(blog *models.Blog) error {
	if DB == nil {
		return errors.New("database not initialized")
	}
	result := DB.Create(blog)
	return result.Error
}

// GetBlog retrieves a blog entry by its ID
func GetBlog(id uint) (*models.Blog, error) {
	if DB == nil {
		return nil, errors.New("database not initialized")
	}
	var blog models.Blog
	result := DB.First(&blog, id)
	if result.Error != nil {
		return nil, result.Error
	}
	return &blog, nil
}

// GetBlogs retrieves all blog entries from the database
func GetBlogs() ([]models.Blog, error) {
	if DB == nil {
		return nil, errors.New("database not initialized")
	}
	var blogs []models.Blog
	result := DB.Find(&blogs)
	if result.Error != nil {
		return nil, result.Error
	}
	return blogs, nil
}

// DeleteBlog deletes a blog entry by its ID
func DeleteBlog(id uint) error {
	if DB == nil {
		return errors.New("database not initialized")
	}
	result := DB.Delete(&models.Blog{}, id)
	return result.Error
}

// user db functions

// function to create a new user
func CreateUserSignup(user *models.User) error {
	if DB == nil {
		return errors.New("database not initialized")
	}
	result := DB.Create(&user)
	return result.Error
}

// function to get all users
// func GetUsers() ([]models.User, error) {
// 	if DB == nil {
// 		return nil, errors.New("database not initialized")
// 	}
// 	var users []models.User
// 	result := DB.Find(&users)
// 	if result.Error != nil {
// 		return nil, result.Error
// 	}
// 	return users, nil
// }

func GetUserLogin(user_email string, user_password string) error {
	if DB == nil {
		return errors.New("database error")
	}

	result := DB.Where("Email = ?, Password = ?", user_email, user_password)
	return result.Error
}
