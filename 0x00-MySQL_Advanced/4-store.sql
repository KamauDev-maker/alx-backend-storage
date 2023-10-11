-- A script that creates a trigger that decreases the quantity of an item after addidng a new order

CREATE TRIGGER decrease_items_quantity AFTER INSERT ON orders FOR EACH ROW
UPDATE items SET quantity = quantity - NEW.number WHERE name=New.item_name;
