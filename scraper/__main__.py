if __name__ == "__main__":
    from .scrape import scrape_tasks

    username = input("What's your SchulCloud E-Mail? ")
    password = input("What's your SchulCloud password? ")
    assignments = scrape_tasks(username=username, password=password)

    print("----")
    for assignment in assignments:
        print(f"{assignment.course} - {assignment.name} (at {assignment.url})")
        print(f"Created: {assignment.created_date} - Due: {assignment.due_date}")
        print(f"{assignment.description}")
        print("----")