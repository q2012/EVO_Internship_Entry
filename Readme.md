# Second task for Evo Internship Entry

First task is on [first brach](https://github.com/q2012/EVO_Internship_Entry/tree/first_task)

----
## Phone assistant
Done using [Trie](https://en.wikipedia.org/wiki/Trie). I wrote very basic implementation with only functions i need. Trie gives speed advantage, especially on large sets, as it has constant time to find a known entry. 

Implementation is by no means ideal, neither in time nor in space, but it is easy-to-understand and working. I did it by myself, as it was computer science task, so doing it using external libraries or simple approaches may be not beneficial. Some of them i listed below.


----
## Usage
Create trie ``` root = Trie()```. Add values(phone strings) using ```add(root, phone_string)```. Take through n phones, that begins with prefix using ``` find_first_n_after_prefix(root, n, prefix_string)```. This returns a generator, so you can iterate through it.

To run tests you need to have pytest installed. Simply run ```pytest tests.py``` or add `-s` for more info


----
## Alternatives

As another trie implementation you can look to [google](https://github.com/google/pygtrie) or [libdartie port](https://github.com/pytries/datrie).

Also, as an easy approach you can simply use filter: ```filter(lambda x: x.startswith(prefix), phone_list)``` which is great, if you don't care about speed.

If phones are in SQL database you could also do something like: ```SELECT ... FROM table WHERE param LIKE 'prefix%'```
