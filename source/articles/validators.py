def validate_article(article):
    errors = {}

    if not article.title:
        errors['title'] = 'Title should not be empty!'
    elif len(article.title) > 10:
        errors['title'] = 'Title should be 200 symbols or less!'

    if not article.author:
        errors['author'] = 'Author should not be empty!'
    elif len(article.author) > 40:
        errors['author'] = 'Author should be 40 symbols or less!'

    if not article.content:
        errors['content'] = 'Content should not be empty!'
    elif len(article.content) > 3000:
        errors['content'] = 'Content should be 3000 symbols or less!'
    return errors