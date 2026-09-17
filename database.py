import pyodbc


# ==========================================
# DATABASE CONNECTION
# ==========================================

def get_connection():
    connection = pyodbc.connect(
        r'DRIVER={ODBC Driver 17 for SQL Server};'
        r'SERVER=Anuj\SQLEXPRESS;'
        r'DATABASE=EXTS;'
        r'Trusted_Connection=yes;'
    )

    return connection

def get_monthly_expense():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            DATENAME(MONTH, ExpenseDate) AS Month,
            SUM(Amount) AS Total
        FROM Expenses
        GROUP BY
            MONTH(ExpenseDate),
            DATENAME(MONTH, ExpenseDate)
        ORDER BY
            MONTH(ExpenseDate)
    """)

    data = cursor.fetchall()

    connection.close()

    return data


# ==========================================
# GET ALL EXPENSES
# ==========================================
def get_balance():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT CurrentBalance
        FROM Wallet
        WHERE WalletID = 1
    """)

    balance = cursor.fetchone()[0]

    connection.close()

    return float(balance)

def get_expenses():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            ExpenseID,
            Title,
            Category,
            Amount,
            ExpenseDate,
            PaymentMethod,
            Description
        FROM Expenses
        ORDER BY ExpenseID DESC
    """)

    expenses = cursor.fetchall()

    connection.close()

    return expenses

# ==========================================
# ADD EXPENSE
# ==========================================

def add_expense(
    title,
    category,
    amount,
    expense_date,
    payment_method,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    # Check available balance
    cursor.execute("""
        SELECT CurrentBalance
        FROM Wallet
        WHERE WalletID = 1
    """)

    balance = float(cursor.fetchone()[0])

    if amount > balance:
        connection.close()
        raise Exception("Insufficient balance!")

    # Insert expense
    cursor.execute("""
        INSERT INTO Expenses
        (
            Title,
            Category,
            Amount,
            ExpenseDate,
            PaymentMethod,
            Description
        )
        VALUES (?, ?, ?, ?, ?, ?)
    """,
        title,
        category,
        amount,
        expense_date,
        payment_method,
        description
    )

    # Deduct from wallet
    cursor.execute("""
        UPDATE Wallet
        SET CurrentBalance = CurrentBalance - ?
        WHERE WalletID = 1
    """, amount)

    connection.commit()
    connection.close()

def delete_expense(expense_id):

    connection = get_connection()
    cursor = connection.cursor()

    # Get expense amount
    cursor.execute("""
        SELECT Amount
        FROM Expenses
        WHERE ExpenseID = ?
    """, expense_id)

    row = cursor.fetchone()

    if row:

        amount = float(row[0])

        # Return money to wallet
        cursor.execute("""
            UPDATE Wallet
            SET CurrentBalance = CurrentBalance + ?
            WHERE WalletID = 1
        """, amount)

        # Delete expense
        cursor.execute("""
            DELETE FROM Expenses
            WHERE ExpenseID = ?
        """, expense_id)

    connection.commit()
    connection.close()

# ==========================================
# UPDATE EXPENSE
# ==========================================

def update_expense(
    expense_id,
    title,
    category,
    amount,
    expense_date,
    payment_method,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    # Get old amount
    cursor.execute("""
        SELECT Amount
        FROM Expenses
        WHERE ExpenseID = ?
    """, expense_id)

    old_amount = float(cursor.fetchone()[0])

    # Update expense
    cursor.execute("""
        UPDATE Expenses
        SET
            Title = ?,
            Category = ?,
            Amount = ?,
            ExpenseDate = ?,
            PaymentMethod = ?,
            Description = ?
        WHERE ExpenseID = ?
    """,
        title,
        category,
        amount,
        expense_date,
        payment_method,
        description,
        expense_id
    )

    difference = amount - old_amount

    # Update wallet balance
    cursor.execute("""
        UPDATE Wallet
        SET CurrentBalance = CurrentBalance - ?
        WHERE WalletID = 1
    """, difference)

    connection.commit()
    connection.close()

# ==========================================
# GET ALL INCOME
# ==========================================

def get_income():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            IncomeID,
            Title,
            Amount,
            IncomeDate,
            Source,
            Description
        FROM Income
        ORDER BY IncomeID DESC
    """)

    income_records = cursor.fetchall()

    connection.close()

    return income_records

# ==========================================
# SAVINGS GOAL
# ==========================================

def add_goal(
    goal_name,
    target_amount,
    recommended_amount,
    reason,
    created_date
):

    connection = get_connection()
    cursor = connection.cursor()

    # Allow only one active goal
    cursor.execute("""
        UPDATE SavingsGoal
        SET IsActive = 0
        WHERE IsActive = 1
    """)

    cursor.execute("""
        INSERT INTO SavingsGoal
        (
            GoalName,
            TargetAmount,
            RecommendedAmount,
            SavedAmount,
            Reason,
            CreatedDate,
            IsActive
        )
        VALUES
        (?, ?, ?, 0, ?, ?, 1)
    """,
        goal_name,
        target_amount,
        recommended_amount,
        reason,
        created_date
    )

    connection.commit()
    connection.close()

def get_active_goal():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT
            GoalID,
            GoalName,
            TargetAmount,
            RecommendedAmount,
            SavedAmount,
            Reason,
            CreatedDate
        FROM SavingsGoal
        WHERE IsActive = 1
    """)

    goal = cursor.fetchone()

    connection.close()

    return goal

def update_goal(
    goal_id,
    goal_name,
    target_amount,
    recommended_amount,
    reason
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE SavingsGoal
        SET
            GoalName = ?,
            TargetAmount = ?,
            RecommendedAmount = ?,
            Reason = ?
        WHERE GoalID = ?
    """,
        goal_name,
        target_amount,
        recommended_amount,
        reason,
        goal_id
    )

    connection.commit()
    connection.close()   

def delete_goal(goal_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE SavingsGoal
        SET IsActive = 0
        WHERE GoalID = ?
    """, goal_id)

    connection.commit()
    connection.close()

def update_saved_amount(
    goal_id,
    amount
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE SavingsGoal
        SET SavedAmount = SavedAmount + ?
        WHERE GoalID = ?
    """,
        amount,
        goal_id
    )

    connection.commit()
    connection.close()

def complete_goal(goal_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE SavingsGoal
        SET IsActive = 0
        WHERE GoalID = ?
    """,
        goal_id
    )

    connection.commit()
    connection.close()

def has_active_goal():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM SavingsGoal
        WHERE IsActive = 1
    """)

    count = cursor.fetchone()[0]

    connection.close()

    return count > 0

# ==========================================
# ADD INCOME
# ==========================================

def add_income(
    title,
    amount,
    income_date,
    source,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    # Save transaction
    cursor.execute("""
        INSERT INTO Income
        (
            Title,
            Amount,
            IncomeDate,
            Source,
            Description
        )
        VALUES (?, ?, ?, ?, ?)
    """,
        title,
        amount,
        income_date,
        source,
        description
    )

    # Increase wallet balance
    cursor.execute("""
        UPDATE Wallet
        SET CurrentBalance = CurrentBalance + ?
        WHERE WalletID = 1
    """, amount)

    connection.commit()
    connection.close()

# ==========================================
# UPDATE INCOME
# ==========================================

def update_income(
    income_id,
    title,
    amount,
    income_date,
    source,
    description
):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        UPDATE Income
        SET
            Title = ?,
            Amount = ?,
            IncomeDate = ?,
            Source = ?,
            Description = ?
        WHERE IncomeID = ?
    """,
        title,
        amount,
        income_date,
        source,
        description,
        income_id
    )

    connection.commit()
    connection.close()


# ==========================================
# DELETE INCOME
# ==========================================

def delete_income(income_id):

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM Income WHERE IncomeID = ?",
        income_id
    )

    connection.commit()
    connection.close()


# ==========================================
# GET TOTAL INCOME
# ==========================================

def get_total_income():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(Amount), 0)
        FROM Income
    """)

    total_income = cursor.fetchone()[0]

    connection.close()

    return float(total_income)


# ==========================================
# GET TOTAL EXPENSE
# ==========================================

def get_total_expense():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        SELECT COALESCE(SUM(Amount), 0)
        FROM Expenses
    """)

    total_expense = cursor.fetchone()[0]

    connection.close()

    return float(total_expense)

# ==========================================
# DATABASE TEST
# ==========================================

if __name__ == "__main__":

    print("=================================")
    print("Testing Expense Tracker Database")
    print("=================================")

    try:

        expenses = get_expenses()

        print("\nDatabase Connected Successfully!")
        print("\nExpenses:\n")

        for expense in expenses:
            print(expense)

        print("\nTotal Income:", get_total_income())
        print("Total Expenses:", get_total_expense())
        print("Balance:", get_balance())

        print("\n=================================")
        print("Database is working!")
        print("=================================")

    except Exception as error:

        print("\nERROR:")
        print(error)

# ==========================================
# GET EXPENSE BY CATEGORY
# ==========================================

def get_expense_by_category():

    # Open database
    connection = get_connection()

    # Make a cursor
    cursor = connection.cursor()

    # Ask SQL to add all expenses in each category
    cursor.execute("""
        SELECT
            Category,
            SUM(Amount)
        FROM Expenses
        GROUP BY Category
    """)

    # Get the answer
    data = cursor.fetchall()

    # Close database
    connection.close()

    # Give data back
    return data