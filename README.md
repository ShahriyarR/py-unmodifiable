# Unmodifiable Lists

This concept is defined and explained in the [Secure by Design](https://www.manning.com/books/secure-by-design) book.

It is also exposed in this link [LiveBook](https://livebook.manning.com/book/secure-by-design/chapter-6/v-6/167).

The overall characteristics can be found in [Book Review: Secure by Design](https://adriancitu.com/2022/10/05/book-review-secure-by-design/)

# From the original [Secure by Design](https://www.manning.com/books/secure-by-design)

The original book is using Java, and it is something like below:

```java
class Order {
    private CustomerID custId;
    private List<OrderLine> orderitems;
    public List<OrderLine> orderItems() {
        return new Collections.unmodifiableList(orderitems);
    }
    }
    List<OrderItem> items = order.orderItems();
    items.add(new OrderItem(SHIPPING_VOUCHER, 1));
```

Well it seems to be something cryptic to you - but the idea is quite simple:

```
Whenever you need to return a List - create immutable/unmodifiable copy of original List and return it back.
In other words, do not share/return mutable objects - it can be mutated and used by lovely attacker guy.
You can of course, return back the deep copy, but as the original book states - it will give a feel or taste that the data can be mutated.
With Unmodifiable Lists - the user/attacker loses the appetite :)
```

# How we can achieve the same concept in Python?

Well, it is quite doable if we enforce some pattern or way of defining our "private" members.

Let's define the rules for our project:

* If there is a "private" list `self.__order_items` there must be corresponding public `order_items` class field
* The public `order_items` must have `ImmutableList` type

Simple, but powerful rules for our project to make sure about data integrity and security.

The sample code is:

```py
from unmodifiable import ImmutableList

class Orders:

    order_items: ImmutableList = []
    
    def __init__(self):
        self.__order_items = ["New Order 1", "New Order 2"]

```

The next is to define public `get_order_items` method to return back unmodifiable/immutable/protected/frozen list:

```py
from unmodifiable import ImmutableList, unmodifiable_list

class Orders:

    order_items: ImmutableList = []
    
    def __init__(self):
        self.__order_items = ["New Order 1", "New Order 2"]
    
    def get_order_items(self):
        with unmodifiable_list(self, "__order_items") as unmodifiable:
            return unmodifiable

```

The `unmodifiable_list` is a context manager, which accepts `self` and the name of target "private" `__order_items` list.

Internally it strips the name `__order_items`,to match the `order_items` - our public ImmutableList.

Then FROM the original private list data will be deep copied(not shallow), 
afterwards this copy will be converted to unmodifiable `FrozenList` type, 
at the end, public `order_items` will be globally updated to get the value of this unmodifiable type.

We can have multiple such data in our class:

```py
from unmodifiable import ImmutableList, unmodifiable_list

class Orders:

    order_items: ImmutableList = []
    old_items = []  # no type hint or wrong type hint provided
    removed_order_items: ImmutableList = []

    def __init__(self):
        self.__order_items = ["New Order 1", "New Order 2"]
        self.__failed_items = ["Failed Order 1", "Failed Order 2"]
        self.__old_items = ["Old Item 1", "Old Item 2"]
        self.__removed_order_items = ["Removed 1", "Removed 2"]

    def get_order_items(self):
        with unmodifiable_list(self, "__order_items") as unmodifiable:
            return unmodifiable

    def get_failed_items(self):
        # This should fail as there is no corresponding public name
        with unmodifiable_list(self, "__failed_items") as unmodifiable:
            return unmodifiable

    def get_old_items(self):
        # This should fail as the corresponding public name has no type hint - it should be ImmutableList
        with unmodifiable_list(self, "__old_items") as unmodifiable:
            return unmodifiable

    def get_removed_order_items(self):
        # This is the same as data from context manager
        with unmodifiable_list(self, "__removed_order_items"):
            return self.removed_order_items
```

# About the Usage

Now let's test it a bit:

```py
>>> orders = Orders()
>>> orders.get_order_items()
>>> orders_ = orders.get_order_items()
>>> orders_
['New Order 1', 'New Order 2']
```

* If you try to append or change the data:

```py
>>> orders_.append("new value")
...
unmodifiable.unmodifiable.UnsupportedOperationException: Not allowed on protected object

>>> orders_[0] = "New Value"
...
unmodifiable.unmodifiable.UnsupportedOperationException: Not allowed on protected object
```

* Trying to access non-typed public object, as a recall, I am going to provide the portion of the class here again:

```py
class Orders:

    order_items: ImmutableList = []
    old_items = []  # no type hint or wrong type hint provided
    removed_order_items: ImmutableList = []

    def get_old_items(self):
        # This should fail as the corresponding public name has no type hint - it should be ImmutableList
        with unmodifiable_list(self, "__old_items") as unmodifiable:
            return unmodifiable
```

If you try to get back `old_items`, it will fail it is not typed as ImmutableList:

```py
>>> orders.get_old_items()
...
AttributeError: Could not find corresponding public field in origin class or it is not type of ImmutableList
```

* Trying to get back unmodifiable  `__failed_items` will also fail as it has no corresponding public `failed_items` object.

```py
class Orders:

    order_items: ImmutableList = []
    old_items = []  # no type hint or wrong type hint provided
    removed_order_items: ImmutableList = []

    def __init__(self):
        self.__order_items = ["New Order 1", "New Order 2"]
        self.__failed_items = ["Failed Order 1", "Failed Order 2"]
        self.__old_items = ["Old Item 1", "Old Item 2"]
        self.__removed_order_items = ["Removed 1", "Removed 2"]

    def get_failed_items(self):
        # This should fail as there is no corresponding public name
        with unmodifiable_list(self, "__failed_items") as unmodifiable:
            return unmodifiable
```

The result:

```py
>>> orders.get_failed_items()
...
AttributeError: Could not find corresponding public field in origin class or it is not type of ImmutableList
```

As you see, we have defined strict rules about our class structure which is a key for ensuring integrity.

Also, defining predefined rules on "How we write classes" or "How secrets should be passed" 
will ensure "Secure by Design" concept beforehand - which is quite powerful mechanism to think about when we write the software.


# How to install for development?

### Create and activate the virtualenv:

* `python3.10 -m venv .venv`

* `source .venv/bin/activate`

We use flit for the package management:

### Install flit:

* `pip install flit==3.7.1`

### Installing project for development

`make install-dev` or `flit install --env --deps=develop --symlink` 

### Installing for general showcase

`make install` or `flit install --env --deps=develop` 

### Run all tests in verbose

`make test` or `pytest -svv` 