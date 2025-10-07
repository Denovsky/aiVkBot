import psycopg2
from psycopg2 import sql

def setup_database():
    conn = psycopg2.connect(
        dbname="postgres",
        user="your_username",
        password="your_password",
        host="localhost"
    )
    conn.autocommit = True
    cur = conn.cursor()
    
    # Создаем тестовую базу данных
    cur.execute("DROP DATABASE IF EXISTS complex_queries_db")
    cur.execute("CREATE DATABASE complex_queries_db")
    cur.close()
    conn.close()
    
    # Подключаемся к новой базе
    conn = psycopg2.connect(
        dbname="complex_queries_db",
        user="your_username",
        password="your_password",
        host="localhost"
    )
    cur = conn.cursor()
    
    # Создаем сложную схему данных
    tables = [
        """
        CREATE TABLE departments (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            budget DECIMAL(15,2),
            created_at TIMESTAMP DEFAULT NOW()
        )
        """,
        """
        CREATE TABLE employees (
            id SERIAL PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            salary DECIMAL(10,2),
            department_id INTEGER REFERENCES departments(id),
            hire_date DATE,
            performance_score INTEGER,
            email VARCHAR(150)
        )
        """,
        """
        CREATE TABLE projects (
            id SERIAL PRIMARY KEY,
            name VARCHAR(200) NOT NULL,
            department_id INTEGER REFERENCES departments(id),
            budget DECIMAL(15,2),
            start_date DATE,
            end_date DATE,
            status VARCHAR(50)
        )
        """,
        """
        CREATE TABLE employee_projects (
            employee_id INTEGER REFERENCES employees(id),
            project_id INTEGER REFERENCES projects(id),
            role VARCHAR(100),
            hours_worked DECIMAL(8,2),
            PRIMARY KEY (employee_id, project_id)
        )
        """,
        """
        CREATE TABLE sales (
            id SERIAL PRIMARY KEY,
            employee_id INTEGER REFERENCES employees(id),
            amount DECIMAL(12,2),
            sale_date DATE,
            product_category VARCHAR(100)
        )
        """
    ]
    
    for table in tables:
        cur.execute(table)
    
    # Вставляем тестовые данные
    insert_data = [
        "INSERT INTO departments (name, budget) VALUES ",
        "('IT', 500000), ('Marketing', 300000), ('Finance', 400000), ('HR', 200000)",
        
        "INSERT INTO employees (name, salary, department_id, hire_date, performance_score, email) VALUES ",
        "('John Smith', 75000, 1, '2020-01-15', 85, 'john@company.com'),",
        "('Maria Garcia', 82000, 1, '2019-03-20', 92, 'maria@company.com'),",
        "('Bob Johnson', 65000, 2, '2021-06-10', 78, 'bob@company.com'),",
        "('Alice Brown', 90000, 3, '2018-11-05', 95, 'alice@company.com')",
        
        "INSERT INTO projects (name, department_id, budget, start_date, end_date, status) VALUES ",
        "('Website Redesign', 1, 100000, '2023-01-01', '2023-06-30', 'active'),",
        "('Product Launch', 2, 150000, '2023-02-01', '2023-08-31', 'active'),",
        "('Financial System', 3, 200000, '2023-03-01', '2023-12-31', 'planned')",
        
        "INSERT INTO employee_projects (employee_id, project_id, role, hours_worked) VALUES ",
        "(1, 1, 'Developer', 120.5), (2, 1, 'Architect', 80.0),",
        "(1, 2, 'Consultant', 40.0), (3, 2, 'Manager', 160.0)",
        
        "INSERT INTO sales (employee_id, amount, sale_date, product_category) VALUES ",
        "(1, 15000, '2023-04-01', 'Software'), (2, 25000, '2023-04-02', 'Hardware'),",
        "(3, 18000, '2023-04-03', 'Services'), (1, 22000, '2023-04-04', 'Software')"
    ]
    
    for query in insert_data:
        if not query.endswith(','):
            cur.execute(query)
    
    conn.commit()
    cur.close()
    conn.close()

if __name__ == "__main__":
    setup_database()

import psycopg2
import psycopg2.extras
from datetime import datetime, timedelta

class ComplexQueryExecutor:
    def __init__(self):
        self.connection = psycopg2.connect(
            dbname="complex_queries_db",
            user="your_username",
            password="your_password",
            host="localhost"
        )
        self.cursor = self.connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    
    def execute_query_1(self):
        # Рекурсивный запрос для поиска иерархии сотрудников по проектам
        query = """
        WITH RECURSIVE project_hierarchy AS (
            SELECT 
                ep.employee_id,
                ep.project_id,
                ep.role,
                1 as level,
                ARRAY[ep.employee_id] as path
            FROM employee_projects ep
            WHERE ep.role = 'Manager'
            
            UNION ALL
            
            SELECT 
                ep.employee_id,
                ep.project_id,
                ep.role,
                ph.level + 1,
                ph.path || ep.employee_id
            FROM employee_projects ep
            JOIN project_hierarchy ph ON ep.project_id = ph.project_id
            WHERE ep.role != 'Manager'
            AND NOT ep.employee_id = ANY(ph.path)
        )
        SELECT 
            p.name as project_name,
            e.name as employee_name,
            ph.role,
            ph.level
        FROM project_hierarchy ph
        JOIN projects p ON p.id = ph.project_id
        JOIN employees e ON e.id = ph.employee_id
        ORDER BY p.name, ph.level, e.name
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_2(self):
        # Аналитическое окно: ранжирование сотрудников по зарплате в департаментах
        query = """
        SELECT 
            d.name as department_name,
            e.name as employee_name,
            e.salary,
            RANK() OVER (PARTITION BY d.id ORDER BY e.salary DESC) as salary_rank,
            AVG(e.salary) OVER (PARTITION BY d.id) as avg_department_salary,
            PERCENT_RANK() OVER (PARTITION BY d.id ORDER BY e.salary) as salary_percentile
        FROM employees e
        JOIN departments d ON e.department_id = d.id
        WHERE e.salary IS NOT NULL
        ORDER BY d.name, salary_rank
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_3(self):
        # Коррелированный подзапрос с агрегатными функциями
        query = """
        SELECT 
            e.name,
            e.salary,
            e.department_id,
            (SELECT COUNT(*) FROM employees e2 
             WHERE e2.department_id = e.department_id 
             AND e2.salary > e.salary) as higher_paid_colleagues,
            (SELECT AVG(salary) FROM employees e3 
             WHERE e3.department_id = e.department_id) as department_avg_salary
        FROM employees e
        WHERE e.salary > (
            SELECT AVG(salary) * 0.8 
            FROM employees e4 
            WHERE e4.department_id = e.department_id
        )
        ORDER BY e.department_id, e.salary DESC
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_4(self):
        # Многомерный агрегатный анализ с ROLLUP
        query = """
        SELECT 
            COALESCE(d.name, 'Все департаменты') as department,
            COALESCE(p.name, 'Все проекты') as project,
            COUNT(DISTINCT ep.employee_id) as employee_count,
            SUM(ep.hours_worked) as total_hours,
            AVG(ep.hours_worked) as avg_hours_per_employee
        FROM employee_projects ep
        JOIN projects p ON p.id = ep.project_id
        JOIN departments d ON p.department_id = d.id
        GROUP BY ROLLUP(d.name, p.name)
        HAVING SUM(ep.hours_worked) > 50
        ORDER BY d.name, p.name
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_5(self):
        # Временной анализ с использованием оконных функций
        query = """
        SELECT 
            s.sale_date,
            e.name as employee_name,
            s.amount,
            SUM(s.amount) OVER (ORDER BY s.sale_date 
                               ROWS BETWEEN 2 PRECEDING AND CURRENT ROW) as moving_avg_3days,
            LAG(s.amount, 1) OVER (PARTITION BY s.employee_id 
                                  ORDER BY s.sale_date) as previous_sale,
            s.amount - LAG(s.amount, 1) OVER (PARTITION BY s.employee_id 
                                             ORDER BY s.sale_date) as sale_growth
        FROM sales s
        JOIN employees e ON e.id = s.employee_id
        WHERE s.sale_date >= CURRENT_DATE - INTERVAL '30 days'
        ORDER BY s.sale_date, e.name
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_6(self):
        # Сложное соединение с условиями и подзапросами
        query = """
        SELECT 
            d.name as department_name,
            COUNT(DISTINCT e.id) as total_employees,
            COUNT(DISTINCT p.id) as active_projects,
            SUM(CASE WHEN e.performance_score > 90 THEN 1 ELSE 0 END) as high_performers,
            (SELECT SUM(s.amount) 
             FROM sales s 
             JOIN employees e2 ON e2.id = s.employee_id 
             WHERE e2.department_id = d.id 
             AND s.sale_date >= CURRENT_DATE - INTERVAL '90 days') as recent_sales
        FROM departments d
        LEFT JOIN employees e ON e.department_id = d.id
        LEFT JOIN projects p ON p.department_id = d.id AND p.status = 'active'
        GROUP BY d.id, d.name
        HAVING COUNT(DISTINCT e.id) > 0
        ORDER BY recent_sales DESC NULLS LAST
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_7(self):
        # Рекурсивный запрос для расчета накопленной статистики
        query = """
        WITH RECURSIVE date_series AS (
            SELECT CURRENT_DATE - 30 as date_day
            UNION ALL
            SELECT date_day + 1
            FROM date_series
            WHERE date_day < CURRENT_DATE
        ),
        daily_sales AS (
            SELECT 
                ds.date_day,
                COALESCE(SUM(s.amount), 0) as daily_total,
                COUNT(s.id) as daily_count
            FROM date_series ds
            LEFT JOIN sales s ON s.sale_date = ds.date_day
            GROUP BY ds.date_day
        ),
        cumulative_sales AS (
            SELECT 
                date_day,
                daily_total,
                daily_count,
                SUM(daily_total) OVER (ORDER BY date_day) as running_total,
                AVG(daily_total) OVER (ORDER BY date_day 
                                      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW) as weekly_moving_avg
            FROM daily_sales
        )
        SELECT * FROM cumulative_sales
        ORDER BY date_day
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def execute_query_8(self):
        # Многопоточный анализ с использованием CTE и оконных функций
        query = """
        WITH department_stats AS (
            SELECT 
                d.id,
                d.name,
                COUNT(e.id) as emp_count,
                AVG(e.salary) as avg_salary,
                MAX(e.performance_score) as max_performance
            FROM departments d
            LEFT JOIN employees e ON e.department_id = d.id
            GROUP BY d.id, d.name
        ),
        project_analysis AS (
            SELECT 
                p.department_id,
                COUNT(p.id) as project_count,
                SUM(p.budget) as total_budget,
                AVG(ep.hours_worked) as avg_hours_per_project
            FROM projects p
            LEFT JOIN employee_projects ep ON ep.project_id = p.id
            GROUP BY p.department_id
        ),
        combined_metrics AS (
            SELECT 
                ds.name as department_name,
                ds.emp_count,
                ds.avg_salary,
                ds.max_performance,
                pa.project_count,
                pa.total_budget,
                pa.avg_hours_per_project,
                RANK() OVER (ORDER BY ds.avg_salary DESC) as salary_rank,
                RANK() OVER (ORDER BY pa.total_budget DESC) as budget_rank
            FROM department_stats ds
            LEFT JOIN project_analysis pa ON pa.department_id = ds.id
        )
        SELECT *,
               (salary_rank + budget_rank) as combined_rank
        FROM combined_metrics
        ORDER BY combined_rank
        """
        
        self.cursor.execute(query)
        return self.cursor.fetchall()
    
    def print_results(self, results, query_name):
        print(f"\n=== Результаты запроса: {query_name} ===")
        for row in results:
            print(dict(row))
    
    def run_all_queries(self):
        queries = [
            ("1. Рекурсивная иерархия проектов", self.execute_query_1),
            ("2. Ранжирование зарплат", self.execute_query_2),
            ("3. Коррелированные подзапросы", self.execute_query_3),
            ("4. Многомерный анализ ROLLUP", self.execute_query_4),
            ("5. Временной анализ продаж", self.execute_query_5),
            ("6. Статистика департаментов", self.execute_query_6),
            ("7. Накопленная статистика", self.execute_query_7),
            ("8. Комплексные метрики", self.execute_query_8)
        ]
        
        for name, query_func in queries:
            try:
                results = query_func()
                self.print_results(results, name)
            except Exception as e:
                print(f"Ошибка в запросе {name}: {e}")
    
    def close(self):
        self.cursor.close()
        self.connection.close()

if __name__ == "__main__":
    executor = ComplexQueryExecutor()
    executor.run_all_queries()
    executor.close()
