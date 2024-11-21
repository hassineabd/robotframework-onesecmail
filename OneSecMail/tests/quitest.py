from OneSecMail.keywords._client import _OneSecMailClient

def main():
    # Créer une instance du client
    client = _OneSecMailClient()
    
    try:
        # Continuer avec le test original
        email = client._generate_temporary_mailbox(count=1)
        print("Email généré :", email)
        
    except Exception as e:
        print(f"Une erreur s'est produite : {e}")
        import traceback
        print(traceback.format_exc())

if __name__ == "__main__":
    main()