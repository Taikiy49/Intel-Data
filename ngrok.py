from pyngrok import ngrok

if __name__ == '__main__':
    public_url = ngrok.connect(5000)
    print(f'Public URL: {public_url}')
    