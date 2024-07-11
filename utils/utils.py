from django.core.exceptions import ValidationError
from django.core.validators import validate_email


def is_valid_email(email):
    try:
        validate_email(email)
        return True
    except ValidationError:
        return False


def save_blog_post(form, request):
    try:
        new_post = form.save(commit=False)
        new_post.author = request.user
        new_post.save()
        messages.success(request, _("Blog post added successfully."))
        return redirect('home')
    except Exception as e:
        logger.error(f"User {request.user.id} failed to add blog post: {str(e)}")
        messages.error(request, _(f"An error occurred: {str(e)}"))
        return render_add_blog_post_form(form)
