from agent import run_agent

def main():
    print("==========================================")
    print("      Simple Safe Shopping Agent CLI      ")
    print("==========================================")
    print("Available Roles: Customer | Admin")
    print("  - Customer: Can search products and check stock")
    print("  - Admin:    Can search products, check stock, and delete items")
    print("==========================================\n")

    role_input = input("Enter your role (Customer/Admin): ").strip().capitalize()
    
    if role_input not in ["Customer", "Admin"]:
        print("Invalid role entered! Defaulting to 'Customer'.\n")
        user_role = "Customer"
    else:
        user_role = role_input

    print(f"\n[Active Session Role: {user_role}]")
    print("Type 'exit' or 'quit' to end the session.\n")

   
    while True:
        user_request = input(f"[{user_role}] Enter your request: ").strip()
        
        if user_request.lower() in ["exit", "quit"]:
            print("Exiting Shopping Agent. Goodbye!")
            break
            
        if not user_request:
            continue

        final_response = run_agent(user_request, user_role=user_role)
        print(f"\nFinal Agent Answer:\n{final_response}\n")
        print("-" * 50)

if __name__ == "__main__":
    main()