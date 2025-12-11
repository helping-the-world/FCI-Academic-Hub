# 🎓 FCI Academic Hub

A comprehensive academic resources hub for the Faculty of Computer Informatics (FCI).

## 🌐 Live Website

Visit: **[Click Me](https://helping-the-world.github.io/FCI-Academic-Hub/)**

## 📚 Features

- 📖 Organized course materials (books, notes, lectures, exams)
- 🎓 4 Academic programs: AI, Cyber Security, Software Engineering, General Hours
- 🔍 Full-text search across all content
- 📱 Responsive design for mobile & desktop
- 🌙 Dark/Light mode toggle

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run local server:**
   ```bash
   mkdocs serve
   ```

3. **Open in browser:** http://127.0.0.1:8000

### Add a New Course

```bash
python3 scripts/create_course.py "Course Name"
```

### Rename a Course

```bash
python3 scripts/rename_course.py old-slug new-slug
```

### Convert MCQ to PDF

```bash
python3 scripts/mcq_to_pdf.py input.txt output.pdf "Quiz Title"
```

📖 See all scripts: **[scripts/README.md](scripts/README.md)**

## 📁 Structure

```
FCI/
├── mkdocs.yml              # MkDocs configuration
├── docs/                   # Documentation source
│   ├── index.md           # Homepage
│   ├── materials/
│   │   ├── courses/       # Individual course pages
│   │   └── curriculum/    # PDF curriculum files
│   └── programs/          # Academic programs (AI, CS, SE, GH)
├── scripts/               # Utility scripts
│   ├── create_course.py   # Create new courses
│   ├── rename_course.py   # Rename courses
│   ├── merge_courses.py   # Merge duplicate courses
│   ├── update_taken_at.py # Update course links
│   └── mcq_to_pdf.py      # MCQ to PDF converter
├── templates/             # Document templates
└── requirements.txt       # Python dependencies
```

## 🔧 Deployment

This site auto-deploys to GitHub Pages when you push to `main` branch.

### Manual Deployment

```bash
mkdocs gh-deploy --force
```

## 🤝 Contributing

Want to contribute? Check out our **[Contribution Guide](CONTRIBUTING.md)** for:

- 📁 Project structure overview
- 📝 File naming conventions
- 📚 How to add new courses & materials
- ✅ PR guidelines

Quick steps:
1. Fork this repository
2. Add your materials following the [naming conventions](CONTRIBUTING.md#file-naming-conventions)
3. Update the course `index.md` with links
4. Submit a pull request

## 📄 License

MIT License - Feel free to use and share!

---

Made with ❤️ by FCI Community
