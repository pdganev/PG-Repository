from flask import Flask, render_template, request, jsonify
import pandas as pd
import sqlite3

app = Flask(__name__)

# Initialize database connection
def init_db():
    # Read the DataFrame and create SQLite database
    df = pd.read_csv('medicines.csv')  # Replace with your data file
    conn = sqlite3.connect('medicines.db')
    df.to_sql('medicines', conn, if_exists='replace', index=False)
    conn.close()

def get_db_connection():
    conn = sqlite3.connect('medicines.db')
    conn.row_factory = sqlite3.Row
    return conn

def get_medicine_substitutes(medicine_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # First get the substitutes list
    query = """
    SELECT substitute0, substitute1, substitute2, substitute3, substitute4
    FROM medicines
    WHERE LOWER(name) = LOWER(?)
    """
    
    cursor.execute(query, (medicine_name,))
    result = cursor.fetchone()
    
    if not result:
        conn.close()
        return []
    
    substitutes = [sub for sub in result if sub and sub.strip()]
    substitute_details = []
    
    for sub in substitutes:
        query = """
        SELECT 
            name,
            price,
            therapeutic_class,
            manufacturer_name,
            short_composition1,
            short_composition2,
            sideEffect0, sideEffect1, sideEffect2, sideEffect3, sideEffect4,
            sideEffect5, sideEffect6, sideEffect7, sideEffect8, sideEffect9,
            sideEffect10, sideEffect11, sideEffect12, sideEffect13, sideEffect14,
            sideEffect15, sideEffect16, sideEffect17, sideEffect18, sideEffect19,
            sideEffect20, sideEffect21, sideEffect22, sideEffect23, sideEffect24,
            sideEffect25, sideEffect26, sideEffect27, sideEffect28, sideEffect29,
            sideEffect30, sideEffect31, sideEffect32, sideEffect33, sideEffect34,
            sideEffect35, sideEffect36, sideEffect37, sideEffect38, sideEffect39,
            sideEffect40, sideEffect41
        FROM medicines
        WHERE LOWER(name) = LOWER(?)
        """
        
        cursor.execute(query, (sub,))
        sub_result = cursor.fetchone()
        
        if sub_result:
            # Process side effects
            side_effects = []
            for i in range(6, 48):  # Indices 6 through 47 contain sideEffect0 through sideEffect41
                if sub_result[i] and sub_result[i].lower() != 'missing':
                    side_effects.append(sub_result[i])
            
            # Process compositions
            compositions = []
            if sub_result[4] and sub_result[4].lower() != 'missing':  # short_composition1
                compositions.append(sub_result[4])
            if sub_result[5] and sub_result[5].lower() != 'missing':  # short_composition2
                compositions.append(sub_result[5])
            
            substitute_details.append({
                "name": sub_result[0],
                "price": sub_result[1],
                "therapeutic_class": sub_result[2],
                "manufacturer": sub_result[3],
                "compositions": compositions,
                "side_effects": side_effects
            })
    
    conn.close()
    return substitute_details



def get_medicine_info(medicine_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = """
    WITH main_medicine AS (
        SELECT 
            name,
            price,
            therapeutic_class,
            manufacturer_name,
            short_composition1,
            short_composition2,
            sideEffect0, sideEffect1, sideEffect2, sideEffect3, sideEffect4,
            sideEffect5, sideEffect6, sideEffect7, sideEffect8, sideEffect9,
            sideEffect10, sideEffect11, sideEffect12, sideEffect13, sideEffect14,
            sideEffect15, sideEffect16, sideEffect17, sideEffect18, sideEffect19,
            sideEffect20, sideEffect21, sideEffect22, sideEffect23, sideEffect24,
            sideEffect25, sideEffect26, sideEffect27, sideEffect28, sideEffect29,
            sideEffect30, sideEffect31, sideEffect32, sideEffect33, sideEffect34,
            sideEffect35, sideEffect36, sideEffect37, sideEffect38, sideEffect39,
            sideEffect40, sideEffect41,
            substitute0, substitute1, substitute2, substitute3, substitute4
        FROM medicines
        WHERE LOWER(name) = LOWER(?)
    )
    SELECT * FROM main_medicine
    """
    
    cursor.execute(query, (medicine_name,))
    main_result = cursor.fetchone()
    
    if not main_result:
        conn.close()
        return None, []
        
    # Process main medicine info
    side_effects = []
    for i in range(42):
        effect = main_result[f'sideEffect{i}']
        if effect and effect.lower() != 'missing':
            side_effects.append(effect)
    
    compositions = []
    if main_result['short_composition1'] and main_result['short_composition1'].lower() != 'missing':
        compositions.append(main_result['short_composition1'])
    if main_result['short_composition2'] and main_result['short_composition2'].lower() != 'missing':
        compositions.append(main_result['short_composition2'])
    
    main_medicine_info = {
        "name": main_result['name'],
        "therapeutic_class": main_result['therapeutic_class'],
        "manufacturer": main_result['manufacturer_name'],
        "price": main_result['price'],
        "compositions": compositions,
        "side_effects": side_effects
    }
    
    # Get substitutes info
    substitutes = get_medicine_substitutes(medicine_name)
    
    conn.close()
    return main_medicine_info, substitutes




@app.route('/autocomplete', methods=['GET'])
def autocomplete():
    search = request.args.get('q')
    if not search or len(search) < 3:
        return jsonify([])
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Case-insensitive search with wildcards
    query = """
    SELECT DISTINCT name 
    FROM medicines 
    WHERE LOWER(name) LIKE LOWER(?) 
    LIMIT 10
    """
    
    cursor.execute(query, (f'{search}%',))
    results = cursor.fetchall()
    conn.close()
    
    return jsonify([row['name'] for row in results])

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        medicine_name = request.form['medicine_name']
        main_medicine, substitutes = get_medicine_info(medicine_name)
        return render_template('result.html', 
                             medicine=main_medicine, 
                             substitutes=substitutes)
    return render_template('index.html')

if __name__ == '__main__':
    # Initialize the database on first run

    # try:
    #     init_db()
    # except Exception as e:
    #     print(f"Database initialization error: {e}")
    
    app.run(debug=True)
