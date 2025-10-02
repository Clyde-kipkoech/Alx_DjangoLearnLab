from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Post, Comment, Tag

from .models import Post, Profile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    class Meta:
        model = User
        fields = ("username", "email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_pic")

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content']
        

class PostForm(forms.ModelForm):
    # show existing tags for multi-select (optional)
    existing_tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Existing tags (select any)"
    )
    # allow user to add new tags as comma-separated text
    new_tags = forms.CharField(
        required=False,
        help_text="Add new tags separated by commas (e.g. django,python)",
        widget=forms.TextInput(attrs={'placeholder': 'tag1, tag2'})
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'existing_tags', 'new_tags']

    def save(self, commit=True, author=None):
        """
        Save Post; attach tags from existing_tags and new_tags.
        If `author` is passed, set post.author before saving.
        """
        post = super().save(commit=False)
        if author is not None:
            post.author = author
        if commit:
            post.save()
        # attach existing tags
        existing = self.cleaned_data.get('existing_tags')
        if existing:
            for t in existing:
                post.tags.add(t)
        # parse and create new tags
        new_tags = self.cleaned_data.get('new_tags', '')
        if new_tags:
            names = [n.strip() for n in new_tags.split(',') if n.strip()]
            for name in names:
                tag_obj, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
                # get_or_create with case-insensitive fallback:
                if created:
                    post.tags.add(tag_obj)
                else:
                    # If get_or_create didn't match due to case, try fetch by name
                    try:
                        t = Tag.objects.get(name__iexact=name)
                        post.tags.add(t)
                    except Tag.DoesNotExist:
                        # fallback: create exact name
                        t = Tag.objects.create(name=name)
                        post.tags.add(t)
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Write your comment...'}),
        }        