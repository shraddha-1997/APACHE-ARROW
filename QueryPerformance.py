import tkinter as tk
from tkinter import messagebox
import sqlite3
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
import time
import psutil

class DataManipulationApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Data Manipulation Comparison")
        
        self.label = tk.Label(root, text="Click the button to compare data manipulation using SQL and Apache Arrow")
        self.label.pack(pady=10)
        
        self.compare_button = tk.Button(root, text="Compare", command=self.compare_data)
        self.compare_button.pack(pady=5)
        
    def memory_usage_psutil(self):
        """Memory usage of the current process in megabytes."""
        process = psutil.Process()
        mem_usage = process.memory_info().rss / (1024 * 1024)  # in MB
        return mem_usage

    def manipulate_data_with_sql(self):
        # Establish connection to the SQLite database file
        conn = sqlite3.connect('employees.db')
        cur = conn.cursor()
        
        # Sample Employee data
        sample_data = pd.DataFrame({'emp_id': range(1, 100001),
                                    'emp_name': ['Employee' + str(i) for i in range(1, 100001)],
                                    'emp_dept': ['Dept' + str(i % 10) for i in range(1, 100001)],
                                    'emp_salary': [50000 + (i % 100) * 100 for i in range(1, 100001)]})
        
        # Create 'employees' table and insert data
        cur.execute('''CREATE TABLE IF NOT EXISTS employees (
                        emp_id INTEGER PRIMARY KEY,
                        emp_name TEXT,
                        emp_dept TEXT,
                        emp_salary REAL
                    )''')
        conn.commit()
        sample_data.to_sql('employees', conn, if_exists='replace', index=False)
        
        before_mem = self.memory_usage_psutil()
        
        start_time = time.time()
        for _ in range(10):  # 10 iterations
            sql_query = "SELECT * FROM employees WHERE emp_salary > 55000"
            sql_result = cur.execute(sql_query).fetchall()
        end_time = time.time()
        
        conn.close()
        
        after_mem = self.memory_usage_psutil()
        mem_usage = after_mem - before_mem
        
        return (end_time - start_time) / 10, mem_usage / 10  # Average time and memory usage per iteration

    def manipulate_data_with_arrow(self):
        # Sample Employee data
        sample_data = pd.DataFrame({'emp_id': range(1, 100001),
                                    'emp_name': ['Employee' + str(i) for i in range(1, 100001)],
                                    'emp_dept': ['Dept' + str(i % 10) for i in range(1, 100001)],
                                    'emp_salary': [50000 + (i % 100) * 100 for i in range(1, 100001)]})
        
        arrow_table = pa.Table.from_pandas(sample_data)
        
        before_mem = self.memory_usage_psutil()
        
        start_time = time.time()
        for _ in range(10):  # 10 iterations
            arrow_result = arrow_table.filter(pc.greater(arrow_table['emp_salary'], 55000))
        end_time = time.time()
        
        after_mem = self.memory_usage_psutil()
        mem_usage = after_mem - before_mem
        
        return (end_time - start_time) / 10, mem_usage / 10  # Average time and memory usage per iteration
    
    def compare_data(self):
        avg_sql_time, avg_sql_mem = self.manipulate_data_with_sql()
        avg_arrow_time, avg_arrow_mem = self.manipulate_data_with_arrow()
        
        messagebox.showinfo("Comparison Results", f"SQL:\nAverage Time: {avg_sql_time} seconds\nAverage Memory usage: {avg_sql_mem:.2f} MB\n\nApache Arrow:\nAverage Time: {avg_arrow_time} seconds\nAverage Memory usage: {avg_arrow_mem:.2f} MB")

if __name__ == "__main__":
    root = tk.Tk()
    app = DataManipulationApp(root)
    root.mainloop()
