from expenses import Expense
import calendar
import datetime


def main():
    print(f"🎯 Running Expense Tracker!")
    expense_file_path = "expenses.csv"
    budget = int(input("Enter your budget: $"))
    while True:
        expense = get_user_expense()
        save_expense_to_file(expense, expense_file_path)

        continue_choice = input(
            "Do you want to add another expense? (y/n): ").lower()

        if continue_choice != "y":
            break
    # Read file and summarize all the expenses
    summarize_expenses(expense_file_path, budget)


def get_user_expense():
    print(f"🎯 Getting User Expense!")
    expense_name = input("Enter expense name: ")
    expense_amount = float(input("Enter expense amount: "))

    expense_categories = [
        "🍕 Food",
        "🏠 Home",
        "💼 Work",
        "🎉 Fun",
        "✨ Misc",
    ]

    while True:
        print("Select a category: ")
        for i, category_name in enumerate(expense_categories):
            print(f"{i+1}. {category_name}")

        value_range = f"[1 - {len(expense_categories)}]"

        try:
            selected_index = int(input(f"Enter a category {value_range}: "))-1

            if selected_index in range(len(expense_categories)):
                selected_category = expense_categories[selected_index]
                new_expense = Expense(
                    name=expense_name, category=selected_category, amount=expense_amount
                )
                return new_expense
            else:
                print("❌ Invalid category. Please try again!")
        except ValueError:
            print("❌ Invalid input. Please enter a number only.")


def save_expense_to_file(expense: Expense, expense_file_path):
    print(f"🎯 Saving User Expense: {expense} to {expense_file_path}")
    with open(expense_file_path, "a", encoding="utf-8") as f:
        f.write(f"{expense.name},{expense.amount},{expense.category}\n")


def summarize_expenses(expense_file_path, budget):
    print(f"🎯 Summarizing User Expense!")
    expenses: list[Expense] = []
    with open(expense_file_path, 'r', encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            expense_name, expense_amount, expense_category = line.strip().split(",")
            line_expense = Expense(
                name=expense_name,
                amount=float(expense_amount),
                category=expense_category,
            )
            expenses.append(line_expense)

    amount_by_category = {}
    for expense in expenses:
        key = expense.category
        if key in amount_by_category:
            amount_by_category[key] += expense.amount
        else:
            amount_by_category[key] = expense.amount
    print("Expenses By Category 📈: ")
    for key, amount in amount_by_category.items():
        print(f" {key}: ${amount:.2f}")

    total_spent = sum([ex.amount for ex in expenses])
    print(f"💵 You've spent ${total_spent:.2f} this month!")

    remaining_budget = budget-total_spent
    if remaining_budget >= 0:
        print(f"✅ Your remaning budget is: ${remaining_budget:.2f}")
    else:
        print("❎ YOU HAVE GOVE OVER BUDGET")

    now = datetime.datetime.now()
    days_in_month = calendar.monthrange(now.year, now.month)[1]
    remaining_days = max(days_in_month-now.day, 1)  # last day of month

    daily_budget = remaining_budget/remaining_days
    print(f"👉🏻 Budget Per Day: ${daily_budget:.2f}")


if __name__ == "__main__":
    main()
