from flask import request, render_template
from db import connect_db

def search_portfolios():
    """ En funktion som hanterar sökningar efter innehåll/portfolios och genererar sökresultatet.
        
        Hämtar söksträng från GET-parameter "query" och söker i databasen efter portfolios,
        där titel eller beskrivning matchar sökordet. 
        Sedan returneras en HTML-sida med resultaten.
        
        Returns: 
                string: En renderad HTML-sida med portfolios som matchar sökningen.
    """
    
    search_input = request.args.get("query", "").strip()
    
    conn = connect_db()
    cur = conn.cursor()
    
    cur.execute("""
                SELECT p.id, p.title, p.description, p.thumbnail, p.created_at, u.username, img.img_path, u.program
                FROM portfolio AS p
                JOIN users AS u ON p.user_id = u.id
                LEFT JOIN portfolio_images AS img ON p.id = img.portfolio_id
                WHERE LOWER(p.title) LIKE LOWER(%s) 
                    OR LOWER(p.description) LIKE LOWER(%s)
                    OR LOWER(u.username) LIKE LOWER(%s)
                    OR LOWER(u.program) LIKE LOWER(%s)
                ORDER BY p.created_at DESC
                """,( 
                    f"%{search_input}%",f"%{search_input}%",
                    f"%{search_input}%",f"%{search_input}%"))
                
    
    portfolios = cur.fetchall()
    cur.close()
    conn.close()
    
    return render_template("search_content.html", portfolios=portfolios, search_input=search_input)