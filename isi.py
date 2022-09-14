
from app import Category, Cars, Type, db

# c1= Category()
# c2= Category()
# c3 = Category()
# c4= Category()
# c5= Category()
# c6 = Category()
# c7 = Category()
# c1.name = "SUV"
# c2.name = "Sedan"
# c3.name = "MPV"
# c4.name = "Hatcback"
# c5.name = "Commercial" 
# c6.name = "Sport" 
# c7.name = "Hybrid" 

# db.session.add_all([c1,c2,c3,c4,c5,c6,c7])
# db.session.commit()





c1= Cars()

c1.name = "Avanza"
c1.price = 250000000
c1.category_id = 3 
c1.colour = "black"

c2= Cars()

c2.name = "Veloz"
c2.price = 350000000
c2.category_id = 3 
c2.colour = "black"

c3= Cars()

c3.name = "AE86"
c3.price = 850000000
c3.category_id = 6
c3.colour = "black"

db.session.add_all([c1,c2,c3])
db.session.commit()