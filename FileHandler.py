from tkinter import filedialog, messagebox
from openpyxl import Workbook


def save_data_to_excel(feedback_data):
    # Create a new workbook
    wb = Workbook()
    # Select the active worksheet
    ws = wb.active

    # Data to insert into the Excel file
    ws.append(['lesson_number', 'student_username', 'teacher_username', 'verbal_feedback', 'quantitative_feedback'])  # Example header
    # Insert data into the worksheet
    for row in feedback_data:
        ws.append(row)

    # Ask the user to choose a location for saving the file
    file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
    if file_path:
        try:
            # Save the workbook
            wb.save(file_path)
            messagebox.showinfo("Success", "Excel file saved successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
