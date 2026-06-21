  
#   custom Exceptions

class InvalidProductError(Exception):
    pass

class InvalidQuantityError(Exception):
    pass

class InvalidMemberTypeError(Exception):
    pass

class InvalidMembershipError(Exception):
    pass

class InvalidPriceError(Exception):
    pass

class InvalidFileError(Exception):
    pass


# Customer Class (Base Class)
class Customer:
    def __init__(self, id, name, value=0):
        # Protected attributes
        self._id = id
        self._name = name
        self._value = value  #total money spent 

    # Getter methods to access attributes
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_value(self):
        return self._value

    # no discount for normal customers
    #the 1st return value represent the rate
    def get_discount(self, price):
        return 0, price
        
        
    # add amount to total customer spending    
    def add_value(self, amount):
        
        self._value += amount

    # Display customer information
    def display_info(self):
        rate, _ = self.get_discount(0) #return (rate , price) and rate,_ means ignore the 2nd value
        print("ID:", self.get_id())
        print("Name:", self.get_name())
        print("Total spent:", self.get_value())
        print("Discount rate:", rate*100, "%")

class Member(Customer):
    # Shared discount rate for all members (default 5%)
    discount_rate= 0.05

    def __init__(self,id,name,value=0):
        # Inherit attributes from Customer class
        super().__init__(id,name,value)

    def get_discount_rate(self):
        return Member.discount_rate
    
    def get_discount(self, price):
        discount_price=price-(price*self.get_discount_rate())
        return self.get_discount_rate(),discount_price
       
    # Display member information
    def display_info(self):
         print("ID: ", self.get_id())
         print("Name: ", self.get_name())
         print("Total spent: ", self.get_value())
         print("Discount rate: ", self.get_discount_rate() * 100, "%")
         


    # Change the shared discount rate for all members
    @classmethod
    def set_rate(cls,new_rate):
        # cls refers to the class itself (Member), not a single object
        cls.discount_rate=new_rate



# VIPMember Class (Subclass)
class VIPMember(Customer):

    # Class variable shared threshold for all VIP members
    _threshold = 1000

    def __init__(self, id, name, value=0, rate1=0.1):
        # Inherit attributes from Customer
        super().__init__(id, name, value)

        # Individual discount rates
        self._rate1 = rate1  #if price <= threshold
        self._rate2 = rate1 + 0.05 #if price > threshold

    #Getter methods
    def get_rate1(self):
        return self._rate1

    def get_rate2(self):
        return self._rate2

    def get_threshold(self):
        return VIPMember._threshold

    # Override method from Customer class
    def get_discount(self, price):
        #different discount based on threshold
        if price <= VIPMember._threshold:
            rate = self._rate1
        else:
            rate = self._rate2
        #Calculate new price after discount
        new_price = price * (1 - rate)
        return rate, new_price

    # Display VIP member information
    def display_info(self):

        print("ID:", self.get_id())
        print("Name:", self.get_name())
        print("Total spent:", self.get_value())
        print("Rate1:",round( self.get_rate1()*100, 1),"%" )
        print("Rate2:",round( self.get_rate2()*100, 1),"%")
        print("Threshold:", self.get_threshold())
        
    #Change discount rates for VIP only
    def set_rate(self, rate1):
        self._rate1 = rate1
        self._rate2 = rate1 + 0.05

    # threshold for ALL VIP members
    @classmethod
    def set_threshold(cls, threshold):
        cls._threshold = threshold

# Product Class
class Product:

    # Constructor
    def __init__(self, product_id, name, price, stock):
        self._id = product_id
        self._name = name
        self._price = float(price)
        self._stock = int(stock)

    # Getter Methods
    def get_id(self):
        return self._id

    def get_name(self):
        return self._name

    def get_price(self):
        return self._price

    def get_stock(self):
        return self._stock


    # Setter Methods
    def set_price(self, new_price):
        self._price = float(new_price)

    def set_stock(self, new_stock):
        self._stock = int(new_stock)

    # Update Stock (Important for Order)
    def reduce_stock(self, quantity):
        self._stock -= quantity

    # Display Method
    def display_info(self):
        print("ID:", self.get_id())
        print("Name:", self.get_name())
        print("Price:", self.get_price(), "SAR")
        print("Stock:", self.get_stock())
        print("-" * 30)


# Order Class
from datetime import datetime

class Order:
    def __init__(self, customer, product, quantity, date=None):

        self._customer = customer
        self._product = product
        self._quantity = int(quantity)

        # Store order date and time
        if date is None:
                self._date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        else:
            self._date = date

    def get_customer(self):
        return self._customer

    def get_product(self):
        return self._product

    def get_quantity(self):
        return self._quantity

    def get_date(self):
        return self._date

    # Calculate original price and discounted price
    def compute_cost(self):

        # Calculate total price before discount
        original_price=self.get_product().get_price()*self.get_quantity()

        # Get discount rate and final price after discount
        discount_rate, discount_price=self.get_customer().get_discount(original_price)

        return original_price,discount_rate, discount_price
    
    # Display order information
    def display_info(self):
        print("Name:", self.get_customer().get_name())
        print("Product:", self.get_product().get_name())
        print("Quantity:", self.get_quantity())

        original_price, discount_rate, discount_price = self.compute_cost()
        print("Real Price:", original_price, "SAR")
        print("Discount Rate:",round( discount_rate*100, 1),"%")
        print("Final Price:", discount_price, "SAR")
        print("-" * 30)
       
    # Process the order and update product stock and customer value
    def process_order(self):

         # Get prices after discount calculation
        original_price, discount_rate, discount_price = self.compute_cost()
         # Check if enough stock is available
        if self.get_quantity() <= self.get_product().get_stock():

             # Update product stock
             new_stock = self.get_product().get_stock() - self.get_quantity()
             self.get_product().set_stock(new_stock)

             # Update customer total spent value
             self.get_customer().add_value(discount_price)

             print("Order processed successfully!")

        else:
            print("Not enough stock available.")
        
        
#  Bundle class special type of Product class
# it contains multiple existing products together
class Bundle(Product):
    def __init__(self, product_id, name, products, stock):
        
        # store products inside the bundle
        self._products = products
        
        # Calculate total price of all products
        total_price = 0
        
        for product in products:
            
            total_price += product.get_price()
            
        # Bundle price = 80% of total products price    
        bundle_price = total_price * 0.8
        
        super().__init__(product_id, name, bundle_price, stock)
        
    # Return all products inside the bundle    
    def get_products(self):
        
        return self._products
        
    # Display bundle information
    def display_info(self):
        
        print("Bundle ID: ", self.get_id())
        print("Name: ", self.get_name())
        
        print("Products inside bundle: ")
        
        # Display IDs of Products inside the bundle
        for product in self._products:
            
            print(product.get_id())
            
        print("Price: ", self.get_price())    
        print("Stock: ", self.get_stock())
                
        
        
# Records Class
class Records:

    # Constructor to create empty lists
    def __init__(self):

        self.customers = []
        self.products = []
        self.orders = []
        
    # generate unique customer ID    
    def generate_id(self, prefix):
        
        max_num = 0
        
        for customer in self.customers:
            
            num = int(customer.get_id()[1:])
            
            if num > max_num:
                max_num = num
                
        return prefix + str(max_num + 1)        

    # Read customers file
    def read_customers(self):

         try:

            file = open("customers.txt", "r")

            for line in file:

                line = line.strip()

                if line == "":
                    continue

                data = line.split(",")
                
                if len(data) != 4:
                    raise InvalidFileError

                customer_id = data[0].strip()
                
                if customer_id[0] not in ["C", "M", "V"]:
                    raise InvalidFileError
                
                
                name = data[1].strip()
                rate = float(data[2].strip())
                value = float(data[3].strip())

                # Normal customer
                if customer_id.startswith("C"):

                    customer = Customer(customer_id, name, value)

                # Member customer
                elif customer_id.startswith("M"):

                    customer = Member(customer_id, name, value)

                    # Set shared discount rate
                    Member.discount_rate = rate

                # VIP customer
                elif customer_id.startswith("V"):

                    customer = VIPMember(customer_id, name, value, rate)

                # Add customer object into list
                self.customers.append(customer)

            file.close()

         except FileNotFoundError:

            print("customers.txt file is missing")
            exit()
            
         except InvalidFileError:
            
            print("Invalid customers file")
            exit()
            
         except:
            
            print("Something is wrong with customers.txt")
            exit()
            
            

        # Read products file
    def read_products(self):

        try:

            file = open("products.txt", "r")

            for line in file:

                line = line.strip()

                if line == "":
                    continue

                data = line.split(",")

                product_id = data[0].strip()
                
                # Normal Product
                
                if product_id.startswith("P"):
                    
                    
                    if len(data) != 4:
                        raise InvalidFileError
                    
                    name = data[1].strip()
                    price = float(data[2].strip())
                    stock = int(data[3].strip())
                    
                    # Create product object
                    product = Product(product_id, name, price, stock)    
                
                    # Add object to products list
                    self.products.append(product)
                    
                # Bundle Product
                elif product_id.startswith("B"):
                    
                    name = data[1].strip()
                    
                    stock = int(data[-1].strip())
                    
                    # get all product IDs inside the bundle start from index 2 until before stock
                    product_ids = data[2:-1]
                    
                    bundle_products = []
                    
                    # Convert product IDs into Product object
                    for pid in product_ids:
                        
                        product = self.find_product(pid.strip())
                        
                        if product is not None:
                            
                            bundle_products.append(product)
                            
                        else:
                            raise InvalidFileError
                            
                    bundle = Bundle(product_id, name, bundle_products, stock)   
                    
                    self.products.append(bundle)
                    
                else:
                    
                    raise InvalidFileError
                    
                    
            file.close()

        except FileNotFoundError:

            print("products.txt file is missing")
            exit()
        except InvalidFileError:
             
             print("Invalid products file")
             exit()
        except:
             
             print("Something is wrong with products.txt")
             exit() 

    # Find customer by ID or name
    def find_customer(self, search_value):

        for customer in self.customers:

            if (customer.get_id().lower() == search_value.lower() or
                    customer.get_name().lower() == search_value.lower()):
                return customer

        return None

    # Find product by ID or name
    def find_product(self, search_value):

        for product in self.products:

            if (product.get_id().lower() == search_value.lower() or
                    product.get_name().lower() == search_value.lower()):
                return product

        return None

    # Display all customers
    def list_customers(self):

        print("\nExisting Customers")
        print("=" * 30)

        for customer in self.customers:
            customer.display_info()
            print("-" * 30)

     # Display all products
    def list_products(self):

        print("\nExisting Products")
        print("=" * 30)

        for product in self.products:
            product.display_info()

    # Load previous orders from orders.txt
    def read_orders(self):

        try:

            file = open("orders.txt", "r")

            for line in file:
                data = line.strip().split(",")

                customer = self.find_customer(data[0].strip())
                product = self.find_product(data[1].strip())
                
                if customer is None or product is None:
                    raise Exception
                    
                    
                quantity = int(data[2].strip())
                date = data[3].strip()

                order = Order(customer, product, quantity, date)

                self.orders.append(order)

            file.close()

        except:

            print("Cannot load the order file. Run as if there is no order previously.")

    # Display all previous orders
    def display_orders(self):

        if len(self.orders) == 0:
            print("No previous orders.")
            return

        for order in self.orders:
            print(order.get_customer().get_name(),
                    order.get_product().get_name(),
                    order.get_quantity(),
                    order.get_date())

    # Display orders of a specific customer
    def display_customer_orders(self, customer_input):

        customer = self.find_customer(customer_input)

        if customer is None:
            print("Invalid customer!")
            return

        found = False

        for order in self.orders:

            if order.get_customer() == customer:
                print(order.get_customer().get_name(),
                      order.get_product().get_name(),
                      order.get_quantity(),
                      order.get_date())

                found = True

        if found == False:
            print("No orders found.")
            
            
            
 

#______________________________________________________________________________

#                          Main Program
#______________________________________________________________________________

import os



# Check if required files exist before running the program
if not os.path.exists("customers.txt"):
    print("customers.txt file is missing")
    exit()

if not os.path.exists("products.txt"):
    print("products.txt file is missing")
    exit()

# Create Records object and load data
records = Records()
records.read_customers()
records.read_products()
records.read_orders()

# Adjust VIP discount rates
def adjust_vip_discount(records):

    customer_input = input("Enter VIP customer name or ID: ")

    customer = records.find_customer(customer_input)

    if customer is None or not isinstance(customer, VIPMember):

        print("Invalid customer!")
        return

    while True:

        try:

            new_rate = float(input("Enter new first discount rate: "))

            if new_rate < 0:
                raise ValueError

            customer.set_rate(new_rate)

            print("Discount updated successfully.")
            break

        except:

            print("Invalid discount rate!")


# Adjust VIP threshold
def adjust_threshold():

    while True:

        try:

            threshold = float(input("Enter new threshold: "))

            if threshold <= 0:
                raise ValueError

            VIPMember.set_threshold(threshold)

            print("Threshold updated successfully.")
            break

        except:

            print("Invalid threshold!")

# Main menu loop
while True:

    # Display menu options
    print("\n------ Menu ------")
    print("1. Place an order")
    print("2. Display existing customers")
    print("3. Display existing products")
    print("4. Adjust VIP discount rates")
    print("5. Adjust VIP threshold")
    print("6. Display all orders")
    print("7. Display all orders of a customer")
    print("8. Exit")

    # Get user choice
    choice = input("Enter your choice: ")


    # Option 1: Place an order
    if choice == "1":
        
        vip_fee = 0

         # Get customer information
        customer_input = input("please enter customer name or ID: ")
        
        # Validate only if input is not an ID
        if not (customer_input.startswith("C") or
                customer_input.startswith("M") or
                customer_input.startswith("V")):
                    
                    if any(char.isdigit() for char in customer_input):
                        
                        print("Customer name cannot contain digits")
                        continue
            
        
        # Find customer in the records
        customer = records.find_customer(customer_input)
        
        # If customer does not exist
        if customer is None:
            
            while True:
                
                
                try:
                    
                    # Ask customer if they want membership
                    answer = input("Do you want membership? (yes/no): ")
                    
                    if answer.lower() not in ["yes" , "no"]:
                        
                        raise InvalidMembershipError
                        
                    break
                
                except InvalidMembershipError:
                    
                    print("please enter yes or no")
                    
                    
                    
            # Normal customer
            if answer.lower() == "no":

                customer_id = records.generate_id("C")
                customer = Customer(customer_id, customer_input)

            # Customer wants membership
            else:
                
                
                while True:
                    
                    try:
                        
                        print("M. Member")
                        print("V. VIP Member")

                        membership_choice = input("Choose membership type ( M / V ): ").upper()
                        
                        if membership_choice not in ["M" , "V"]:
                            
                            raise InvalidMemberTypeError
                            
                        break
                    
                     
                    except InvalidMemberTypeError:
                        
                         
                        print("Invalid membership type!")
                        print("Please enter M for Member or V for VIP Member")

                        
                    

                # Create normal member
                if membership_choice == "M":

                    member_id = records.generate_id("M")
                    customer = Member(member_id, customer_input)
                    
                    

                # Create VIP member
                else:

                    vip_id = records.generate_id("V")
                    customer = VIPMember(vip_id, customer_input)

                    # Add VIP membership fee
                    vip_fee = 200

            # Add new customer to records ****** 
            records.customers.append(customer)
         
            
        # Product Validation
        #keep asking until user enters a valid product
        while True:
            
            try:
                
                product_input = input("Enter product name or ID: ")
                
                # search for product
                product = records.find_product(product_input)
                
                # Raise error if product doesn't exist
                if product is None:
                    
                    raise InvalidProductError
                    
                # Raise error if product price is invalid   
                if product.get_price() <= 0:
                    
                    raise InvalidPriceError
                    
                break
            
            except InvalidProductError:
                
                print("product does not exist")
                
            except InvalidPriceError:
                
                print("invalid product price")
                
                product = None
                
                break
            
        if product is None:
            continue
            
        # Quantity Validation
        
        while True:
            try:
                
                quantity = int(input("Enter quantity: "))
                
                if quantity <= 0:
                    
                    raise InvalidQuantityError
                    
                if quantity > product.get_stock():
                    
                    raise InvalidQuantityError
                    
                break
            
            except ValueError:
                
                print("Quantity must be integer")
                
            except InvalidQuantityError:
                
                print("invalid quantity")
                
                
                
        # Create order object
        order = Order(customer, product, quantity)

        # Display order details
        order.display_info()

        # Process the order
        order.process_order()
        records.orders.append(order)
        
        
        if vip_fee > 0:
            
            customer.add_value(vip_fee)
            
            print("Membership price: ", vip_fee , "SAR")
            
            print("Final total with VIP membership: ", order.compute_cost()[2] + vip_fee, "SAR")

    # Option 2: Display existing customers
    elif choice == "2":

        records.list_customers()

    # Option 3: Display existing products
    elif choice == "3":

        records.list_products()

    # Option 4: Adjust VIP discount rates
    elif choice == "4":

        adjust_vip_discount(records)
 

    # Option 5: Adjust VIP threshold
    elif choice == "5":

        adjust_threshold()

     # Option 6: Display all orders
    elif choice == "6":

        records.display_orders()

     # Option 7: Display all orders of a customer
    elif choice == "7":

        customer_input = input("Enter customer name or ID: ")

        records.display_customer_orders(customer_input)

    # Option 8: Exit program
    elif choice == "8":

        print("Program ended.")
        break


    # Invalid choice
    else:

        print("Invalid choice")
        
        
        
        
        
        