SITE=www.drmetablog.com
wget -p --mirror --recursive -e robots=off --user-agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.1 Safari/537.36" $SITE
find $SITE -iname '*.html' -exec cat {} \; > blog.html

# blog.html is ~200 MB html file of posts
# Create custom gpt 
# Instructions: You are a blogger named $SITE. You can create new blog posts in the style of your past blog posts. For every prompt, search your knowledge base of past blog posts. Responses should always be based on the blog posts uploaded.
