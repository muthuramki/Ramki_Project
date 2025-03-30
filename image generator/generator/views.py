from django.shortcuts import render
import openai
from django.conf import settings
from django.http import JsonResponse

openai.api_key = settings.OPENAI_API_KEY

def generate_image(request):
    if request.method == 'POST':
        description = request.POST.get('description')
        try:
            # Generate image using OpenAI API
            response = openai.Image.create(
                prompt=description,
                n=1,
                size="1024x1024"
            )
            image_url = response['data'][0]['url']
            # Return the image URL as a JSON response to be handled by JavaScript
            return JsonResponse({'image_url': image_url})
        except Exception as e:
            # Handle potential errors (e.g., API errors)
            return JsonResponse({'error': str(e)}, status=500)

    # If GET request, simply render the template
    return render(request, 'image_generator.html', {
        'images': []  # Replace this with a queryset of pre-existing images if needed
    })
