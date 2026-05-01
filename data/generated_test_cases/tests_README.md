## Test Case 1: Basic Formatting
**Purpose:** Check simple text formatting with headers and emphasis

### Input:
```markdown
## Sample Header
### Subheader Example
This is a **bold** text and this is an *italic* text.
```

### Expected:
- Header 2
- Header 3
- Bold text
- Italic text

---

## Test Case 2: Image and Links
**Purpose:** Validate image rendering and hyperlink functionality

### Input:
```markdown
![Sample Image](https://example.com/image.png)
Visit [Example Site](https://example.com) for more info.
```

### Expected:
- Image with source
- Hyperlink with URL

---

## Test Case 3: Nested Lists
**Purpose:** Evaluate nested list rendering

### Input:
```markdown
- Item 1
  - Subitem 1.1
  - Subitem 1.2
- Item 2
```

### Expected:
- Unordered list
- Nested list

---

## Test Case 4: Mixed Formatting
**Purpose:** Test a mix of elements including lists and emphasis

### Input:
```markdown
### List Example
- **Bold Item**
- *Italic Item*
  - Subitem with **bold** and *italic*
```

### Expected:
- Header 3
- Bold text in list
- Italic text in list
- Nested list with formatting

---

## Test Case 5: Table Structure
**Purpose:** Verify table structure parsing

### Input:
```markdown
| Header 1 | Header 2 |
|----------|----------|
| Cell 1   | Cell 2   |
| Cell 3   | Cell 4   |
```

### Expected:
- Table with headers
- Table cells

---

## Test Case 6: Blockquotes
**Purpose:** Confirm blockquote rendering

### Input:
```markdown
> This is a blockquote.
> It extends to multiple lines.
```

### Expected:
- Blockquote

---

## Test Case 7: Code Blocks
**Purpose:** Validate code block formatting

### Input:
```markdown
```
def hello_world():
    print("Hello, world!")
```
```

### Expected:
- Code block

---

## Test Case 8: Mixed Content
**Purpose:** Check complex Markdown with various elements

### Input:
```markdown
## Heading
Text with [link](https://example.com) and ![image](https://example.com/image.png).

- List item
  - **Bold** subitem
```

### Expected:
- Header
- Link
- Image
- List
- Nested list with bold text

---

## Test Case 9: Italic and Bold Combinations
**Purpose:** Test combinations of bold and italic text

### Input:
```markdown
This is *italic* and **bold** and ***both***.
```

### Expected:
- Italic text
- Bold text
- Combined bold and italic text

---

## Test Case 10: Complex Table
**Purpose:** Validate complex table with formatting

### Input:
```markdown
| **Bold** | *Italic* |
|----------|----------|
| Cell 1   | Cell 2   |
| ***Both***| Cell 4  |
```

### Expected:
- Table with headers
- Bold and italic in table

---

## Test Case 11: Basic Formatting
**Purpose:** Test basic text formatting with headers, bold, and italic.

### Input:
```markdown
## Welcome to Markdown Testing
This is a **bold** statement and *italic* text. Explore more!
```

### Expected:
- Header level 2
- Bold text
- Italic text

---

## Test Case 12: Lists and Links
**Purpose:** Verify unordered lists and hyperlink rendering.

### Input:
```markdown
### Useful Resources
- [Markdown Guide](https://www.markdownguide.org)
- [GitHub](https://github.com)
- [Stack Overflow](https://stackoverflow.com)
```

### Expected:
- Header level 3
- Unordered list
- Three hyperlinks

---

## Test Case 13: Images and Captions
**Purpose:** Validate image embedding with captions.

### Input:
```markdown
### Beautiful Landscape
![Landscape](https://example.com/landscape.png)  
*Nature at its best.*
```

### Expected:
- Header level 3
- Image with URL
- Caption in italic

---

## Test Case 14: Ordered List and Emphasis
**Purpose:** Test ordered lists with emphasized text.

### Input:
```markdown
## Steps to Success
1. **Plan** your tasks
2. *Execute* them diligently
3. **Review** and improve
```

### Expected:
- Header level 2
- Ordered list
- Bold and italic text

---

## Test Case 15: Tables and Mixed Formatting
**Purpose:** Check table layout and mixed text formatting.

### Input:
```markdown
## Product Comparison
| Product  | Price | **Rating** |
|----------|-------|------------|
| Item A   | $10   | *4 stars*  |
| Item B   | $15   | **5 stars**|
```

### Expected:
- Header level 2
- Table with three columns
- Bold and italic text in table

---

## Test Case 16: Nested Lists
**Purpose:** Validate nested list rendering.

### Input:
```markdown
### Shopping List
- Fruits
  - Apples
  - Bananas
- Vegetables
  - Carrots
  - Broccoli
```

### Expected:
- Header level 3
- Nested unordered list

---

## Test Case 17: Blockquotes and Links
**Purpose:** Test blockquotes with embedded links.

### Input:
```markdown
## Inspirational Quote
> "The best way to predict the future is to [create](https://example.com) it." — Abraham Lincoln
```

### Expected:
- Header level 2
- Blockquote
- Hyperlink within blockquote

---

## Test Case 18: Code Blocks and Inline Code
**Purpose:** Ensure code blocks and inline code are formatted correctly.

### Input:
```markdown
### Code Snippets
To display `Hello World`, use:
```python
print("Hello World")
```
```

### Expected:
- Header level 3
- Inline code
- Code block

---

## Test Case 19: Mixed Content with Lists and Code
**Purpose:** Examine mixed content including lists and inline code.

### Input:
```markdown
## Learning Markdown
- Use `#` for headers
- Use `*` or `_` for *italic*
- Use `**` for **bold**
```

### Expected:
- Header level 2
- Unordered list
- Inline code segments

---

## Test Case 20: Advanced Table Layout
**Purpose:** Confirm complex table formatting.

### Input:
```markdown
## Monthly Budget
| Category    | Budget | Actual  | Variance |
|-------------|--------|---------|----------|
| Rent        | $1000  | $1000   | $0       |
| Groceries   | $300   | $350    | **-$50** |
| Utilities   | $200   | $180    | *$20*    |
```

### Expected:
- Header level 2
- Table with four columns
- Bold and italic text in table

---

## Test Case 21: Simple Documentation
**Purpose:** Verify rendering of headers, lists, and links.

### Input:
```markdown
## Features
1. Easy to use
2. Cross-platform

### Learn More
Visit the [official site](https://markdown-here.com) for details.
```

### Expected:
- Header for "Features"
- Ordered list
- Sub-header for "Learn More"
- Clickable link

---

## Test Case 22: Image and Text
**Purpose:** Check image embedding alongside text.

### Input:
```markdown
## Welcome to Markdown Here

![Markdown Logo](https://raw.github.com/adam-p/markdown-here/master/src/common/images/icon48.png)

Make your emails stylish!
```

### Expected:
- Header "Welcome to Markdown Here"
- Display of image
- Text paragraph

---

## Test Case 23: Mixed Formatting
**Purpose:** Test mixed text formatting (bold, italic).

### Input:
```markdown
## Markdown Styling

**Bold Text** enhances emphasis. *Italic Text* adds subtlety.
```

### Expected:
- Header "Markdown Styling"
- Bold text rendered
- Italic text rendered

---

## Test Case 24: Nested Lists
**Purpose:** Verify nested list rendering.

### Input:
```markdown
## To-Do List
1. **Groceries**
   - Milk
   - Bread
2. *Work Tasks*
   - Emails
   - Meeting
```

### Expected:
- Header "To-Do List"
- Ordered list with bold and italic text
- Nested unordered lists

---

## Test Case 25: Contact Information
**Purpose:** Verify table rendering for structured data.

### Input:
```markdown
## Contact Info

| Name     | Email                   |
|----------|-------------------------|
| John Doe | john.doe@example.com    |
| Jane Doe | jane.doe@example.com    |
```

### Expected:
- Header "Contact Info"
- Table with headers and data

---

## Test Case 26: Code Snippets
**Purpose:** Evaluate code block display.

### Input:
```markdown
## Sample Code

```python
def hello_world():
    print("Hello, World!")
```
```

### Expected:
- Header "Sample Code"
- Correctly formatted code block

---

## Test Case 27: Recipe Format
**Purpose:** Check list and sub-header combination.

### Input:
```markdown
## Recipe: Pancakes

### Ingredients
- 1 cup flour
- 2 eggs
```

### Expected:
- Header "Recipe: Pancakes"
- Sub-header "Ingredients"
- Unordered list

---

## Test Case 28: Link and Image Together
**Purpose:** Verify that links and images can coexist.

### Input:
```markdown
## Explore

![Logo](https://raw.github.com/adam-p/markdown-here/master/src/common/images/icon48.png)

Visit our [website](https://markdown-here.com).
```

### Expected:
- Header "Explore"
- Image displayed
- Clickable link

---

## Test Case 29: Business Card
**Purpose:** Test formatting with inline elements.

### Input:
```markdown
## Business Card

**Name:** John Doe  
**Email:** john.doe@example.com
```

### Expected:
- Header "Business Card"
- Bold inline elements
- Line breaks

---

## Test Case 30: Event Schedule
**Purpose:** Verify bullet list and bold text.

### Input:
```markdown
## Event Schedule

- **9 AM:** Registration
- **10 AM:** Opening Speech
```

### Expected:
- Header "Event Schedule"
- Unordered list with bold text


## Test Case 31: Simple Document with Header and List
**Purpose:** Test basic header and unordered list rendering

### Input:
```markdown
## Shopping List
- Bread
- Milk
- Eggs
```

### Expected:
- Second-level header
- Unordered list with three items

---

## Test Case 32: Mixed Formatting with Links
**Purpose:** Test bold, italic, and link rendering

### Input:
```markdown
### Resources
Visit the [**official site**](https://example.com) for more info.  
*Italic text* and **bold text** are important.
```

### Expected:
- Third-level header
- Hyperlink
- Italic text
- Bold text

---

## Test Case 33: Image and Caption
**Purpose:** Test image inclusion with alt text

### Input:
```markdown
![Sunset](https://example.com/sunset.jpg)
Caption: **Beautiful Sunset**
```

### Expected:
- Image with alt text "Sunset"
- Bold caption text

---

## Test Case 34: Nested Lists
**Purpose:** Test nested list rendering

### Input:
```markdown
#### Tasks
- Morning
  - Breakfast
  - Workout
- Evening
  - Dinner
  - Relax
```

### Expected:
- Fourth-level header
- Nested unordered lists

---

## Test Case 35: Table Structure
**Purpose:** Test table formatting

### Input:
```markdown
| Name  | Age | City     |
|-------|-----|----------|
| John  | 28  | New York |
| Alice | 30  | Paris    |
```

### Expected:
- Table with headers and two rows

---

## Test Case 36: Blockquote with Formatting
**Purpose:** Test blockquote containing formatted text

### Input:
```markdown
> ### Quote of the Day
> "Imagination is more important than knowledge." — *Albert Einstein*
```

### Expected:
- Blockquote
- Third-level header
- Italicized text

---

## Test Case 37: Combined Elements
**Purpose:** Test combined markdown elements in a single document

### Input:
```markdown
## Welcome to Markdown
Explore the world of **Markdown**. Visit [our page](https://example.com).  
![Icon](https://example.com/icon.png)  
- Quick
- Simple
```

### Expected:
- Second-level header
- Bold text
- Hyperlink
- Image
- Unordered list

---

## Test Case 38: Italics and Code Block
**Purpose:** Test italicized text and code block

### Input:
```markdown
*Italic note*: Use the following code:
```
print("Hello, World!")
```
```

### Expected:
- Italicized text
- Code block

---

## Test Case 39: Multi-level Headers
**Purpose:** Test rendering of various header levels

### Input:
```markdown
# Main Title
## Subtitle
### Section
#### Subsection
##### Detail
```

### Expected:
- Headers from first to fifth level

---

## Test Case 40: Checklist Format
**Purpose:** Test checklist rendering

### Input:
```markdown
#### To-Do List
- [x] Write tests
- [ ] Review code
- [ ] Submit report
```

### Expected:
- Fourth-level header
- Checklist with three items (two unchecked, one checked)

---

## Test Case 41: Simple Document Structure
**Purpose:** Test basic document structure with headers and lists.

### Input:
```markdown
## Introduction
Welcome to the Markdown test.

### Features
- Easy to use
- Lightweight
- Cross-platform

### Conclusion
Markdown is a versatile tool for documentation.
```

### Expected:
- Header: Introduction
- Sub-header: Features, Conclusion
- Bullet list: Easy to use, Lightweight, Cross-platform

---

## Test Case 42: Image and Links
**Purpose:** Ensure images and links render correctly.

### Input:
```markdown
![Sample Image](https://example.com/image.png)

[Visit Example](https://example.com)

### Links
- [Google](https://google.com)
- [Yahoo](https://yahoo.com)
```

### Expected:
- Image with URL: https://example.com/image.png
- Link: Visit Example, Google, Yahoo

---

## Test Case 43: Text Formatting
**Purpose:** Validate bold and italic text rendering.

### Input:
```markdown
This is **bold text** and this is *italic text*.

### Combination
- **Bold and *italic***
- ***Bold and italic***
```

### Expected:
- Bold text: "bold text"
- Italic text: "italic text"
- Combination: Bold and italic

---

## Test Case 44: Nested Lists
**Purpose:** Test nested list structures.

### Input:
```markdown
### Grocery List
- Fruits
  - Apples
  - Oranges
- Vegetables
  - Carrots
  - Spinach
```

### Expected:
- Header: Grocery List
- Nested list structure

---

## Test Case 45: Tables
**Purpose:** Validate table rendering.

### Input:
```markdown
### Pricing Table
| Product  | Price |
|----------|-------|
| Apples   | $1    |
| Oranges  | $2    |
```

### Expected:
- Header: Pricing Table
- Table with columns: Product, Price

---

## Test Case 46: Blockquotes
**Purpose:** Ensure blockquotes are displayed correctly.

### Input:
```markdown
### Famous Quote
> "The only way to do great work is to love what you do." - Steve Jobs
```

### Expected:
- Header: Famous Quote
- Blockquote with text

---

## Test Case 47: Code Blocks
**Purpose:** Test rendering of code blocks.

### Input:
```markdown
### Sample Code
```python
def hello_world():
    print("Hello, world!")
```
```

### Expected:
- Header: Sample Code
- Code block with Python syntax

---

## Test Case 48: Multiple Headers
**Purpose:** Validate different header levels.

### Input:
```markdown
## Main Header
### Sub Header 1
Content under subheader 1.

### Sub Header 2
Content under subheader 2.
```

### Expected:
- Main Header
- Sub Header 1, Sub Header 2

---

## Test Case 49: Mixed Content
**Purpose:** Test rendering of mixed Markdown elements.

### Input:
```markdown
## Welcome
### About Us
We use **Markdown** for *documentation*.

![Logo](https://example.com/logo.png)

- [Contact Us](https://example.com/contact)
```

### Expected:
- Headers: Welcome, About Us
- Bold, Italic text
- Image, Link

---

## Test Case 50: Complex Document
**Purpose:** Ensure complex documents are processed correctly.

### Input:
```markdown
## Project Overview
**Objective:** Improve user experience.

### Tasks
- Research
  - User Interviews
  - Market Analysis
- Development
  - Prototyping
  - Testing

### Summary
> "Understanding user needs is crucial."

[Read More](https://example.com/details)
```

### Expected:
- Header: Project Overview, Tasks, Summary
- Bold, Nested lists, Blockquote
- Link with URL

---

## Test Case 51: Product Feature List
**Purpose:** To test rendering of various Markdown list types and text formatting.

### Input:
```markdown
## Product Features
- **High Performance**: Our product is built for speed.
- *User Friendly*: Easy to navigate interface.
- **Affordable**: Competitive pricing.

### Advantages
1. **Reliability**
2. *Efficiency*
3. **Security**
```

### Expected:
- Rendered headings
- Bold and italic text
- Unordered and ordered lists

---

## Test Case 52: Simple Table with Links
**Purpose:** To check the rendering of tables and hyperlinks.

### Input:
```markdown
### Resources Table
| Resource | Link |
| -------- | ---- |
| **GitHub** | [Visit GitHub](https://github.com) |
| *Google* | [Search](https://google.com) |

#### Note
- Links should be clickable
```

### Expected:
- Rendered table with links
- Bold and italic text

---

## Test Case 53: Image and Description
**Purpose:** To validate image rendering and text formatting.

### Input:
```markdown
## Company Logo
![Company Logo](https://example.com/logo.png)

### Description
Our **company** logo represents *trust* and **innovation**.
```

### Expected:
- Rendered image
- Header and formatted text

---

## Test Case 54: Nested Lists
**Purpose:** To test nested list rendering.

### Input:
```markdown
## Shopping List
- Fruits
  - Apple
  - Banana
- Vegetables
  - Carrot
  - Spinach

### Note
- List should be properly nested
```

### Expected:
- Rendered nested lists

---

## Test Case 55: Mixed Formatting in List
**Purpose:** To test mixed text formatting within lists.

### Input:
```markdown
### Tasks
1. **Complete** the project
2. *Review* the document
3. **Submit** the report

#### Conclusion
- Lists with mixed formatting should render correctly
```

### Expected:
- Ordered list with mixed formatting

---

## Test Case 56: FAQ Section
**Purpose:** To validate question-answer format using Markdown.

### Input:
```markdown
## Frequently Asked Questions

### What is Markdown?
Markdown is a lightweight markup language for creating formatted text using a plain-text editor.

### How to use it?
1. **Write** your content
2. *Format* using Markdown syntax
3. **Preview** and share
```

### Expected:
- Rendered headers and lists
- Proper text formatting

---

## Test Case 57: Contact Information
**Purpose:** To test Markdown rendering of contact details with links and lists.

### Input:
```markdown
## Contact Us

- **Email**: [info@example.com](mailto:info@example.com)
- **Phone**: *123-456-7890*
- **Address**: 123 Example Street, Example City

### Business Hours
- Monday to Friday: **9 AM - 5 PM**
```

### Expected:
- Rendered links and formatted text
- List rendering

---

## Test Case 58: Event Schedule
**Purpose:** To check rendering of event schedules using tables.

### Input:
```markdown
## Event Schedule

| **Day** | **Event** |
| ------- | --------- |
| Monday  | Opening Ceremony |
| *Tuesday* | Workshop 1 |

### Note
- Table should render correctly
```

### Expected:
- Rendered table with bold and italic text

---

## Test Case 59: Markdown Syntax Highlight
**Purpose:** To test rendering of code blocks and inline code.

### Input:
```markdown
## Code Example

```javascript
function greet() {
  return "Hello, World!";
}
```

### Inline Example
- Use the `greet()` function to display a message.
```

### Expected:
- Rendered code block and inline code
- Header rendering

---

## Test Case 60: Team Introduction
**Purpose:** To test rendering of headers, lists, and images.

### Input:
```markdown
## Meet the Team

### John Doe
![John Doe](https://example.com/johndoe.png)
- **Role**: Developer
- *Interests*: Coding, Music

### Jane Smith
- **Role**: Designer
- *Interests*: Art, Photography
```

### Expected:
- Rendered images and headers
- List with bold and italic text

## Test Case 61: Blog Post Structure
**Purpose:** Test a common blog post format with headers, links, and images.

### Input:
```markdown
## Welcome to My Blog
![Blog Banner](https://example.com/banner.png)
### Introduction
Thank you for visiting! Check out my [latest post](https://example.com/post).

### What I Write About
- Technology
- Travel
- Food
```

### Expected:
- Header "Welcome to My Blog"
- Image with alt "Blog Banner"
- Subheaders "Introduction" and "What I Write About"
- Link to latest post
- Bullet list

---

## Test Case 62: Recipe Format
**Purpose:** Test a markdown for a recipe with lists and images.

### Input:
```markdown
## Delicious Pancakes
![Pancakes Image](https://example.com/pancakes.png)
### Ingredients
- 1 cup flour
- 2 eggs
- 1 cup milk

### Instructions
1. Mix all ingredients.
2. Cook on a hot griddle.
3. Serve warm.
```

### Expected:
- Header "Delicious Pancakes"
- Image with alt "Pancakes Image"
- Subheaders "Ingredients" and "Instructions"
- Bullet list for ingredients
- Numbered list for instructions

---

## Test Case 63: Simple Documentation
**Purpose:** Check markdown for a basic documentation page with tables.

### Input:
```markdown
## Product Documentation
### Features
- Easy to use
- High performance

### Specifications
| Feature | Description |
|---------|-------------|
| Speed   | Fast        |
| Usage   | Simple      |
```

### Expected:
- Header "Product Documentation"
- Subheaders "Features" and "Specifications"
- Bullet list of features
- Table with two columns and two rows

---

## Test Case 64: Project Showcase
**Purpose:** Test markdown for showcasing a project with images and links.

### Input:
```markdown
## Project X
![Project Logo](https://example.com/logo.png)
### Overview
Project X is a revolutionary new tool.
[See more details](https://example.com/details).

### Features
- Innovative design
- User-friendly interface
```

### Expected:
- Header "Project X"
- Image with alt "Project Logo"
- Subheaders "Overview" and "Features"
- Link to more details
- Bullet list of features

---

## Test Case 65: Travel Diary Entry
**Purpose:** Test markdown for a travel diary with links and images.

### Input:
```markdown
## Trip to Paris
![Eiffel Tower](https://example.com/eiffel.png)
### Day 1
Visited the Eiffel Tower. [Learn more](https://example.com/eiffel).

### Highlights
- Stunning views
- Delicious pastries
```

### Expected:
- Header "Trip to Paris"
- Image with alt "Eiffel Tower"
- Subheaders "Day 1" and "Highlights"
- Link to learn more about the Eiffel Tower
- Bullet list of highlights

---

## Test Case 66: Meeting Notes
**Purpose:** Test markdown for formatting meeting notes with lists.

### Input:
```markdown
## Team Meeting - October 2023
### Agenda
1. Review last quarter performance
2. Discuss new project proposals

### Attendees
- Alice
- Bob
- Charlie
```

### Expected:
- Header "Team Meeting - October 2023"
- Subheaders "Agenda" and "Attendees"
- Numbered list for agenda
- Bullet list for attendees

---

## Test Case 67: Book Review
**Purpose:** Test markdown for a book review with italic and bold text.

### Input:
```markdown
## Book Review: *The Great Novel*
**Author:** John Doe

### Summary
*The Great Novel* is an exciting story about adventure and discovery.

### Verdict
**Highly recommended!**
```

### Expected:
- Header "Book Review: The Great Novel"
- Italicized book title
- Bold "Author" and "Highly recommended!"
- Subheaders "Summary" and "Verdict"

---

## Test Case 68: Conference Announcement
**Purpose:** Test markdown for announcing a conference with links and lists.

### Input:
```markdown
## Tech Conference 2023
### Details
Join us for the [Tech Conference 2023](https://example.com/conference).
- Date: March 15-17
- Location: San Francisco

### Topics
- AI advancements
- Cybersecurity
```

### Expected:
- Header "Tech Conference 2023"
- Subheaders "Details" and "Topics"
- Link to the conference page
- Bullet list for details and topics

---

## Test Case 69: Fitness Routine
**Purpose:** Test markdown for a weekly fitness routine with lists.

### Input:
```markdown
## Weekly Fitness Routine
### Monday
- Cardio: 30 minutes
- Strength: 20 minutes

### Wednesday
- Yoga: 45 minutes
- Meditation: 15 minutes
```

### Expected:
- Header "Weekly Fitness Routine"
- Subheaders "Monday" and "Wednesday"
- Bullet lists for each day's activities

---

## Test Case 70: Music Album Release
**Purpose:** Test markdown for announcing a music album release with links and images.

### Input:
```markdown
## New Album: *Sounds of Nature*
![Album Cover](https://example.com/album.png)
### Release Date
November 2023

### Listen Now
[Stream on Spotify](https://example.com/spotify)
```

### Expected:
- Header "New Album: Sounds of Nature"
- Image with alt "Album Cover"
- Subheaders "Release Date" and "Listen Now"
- Link to stream on Spotify