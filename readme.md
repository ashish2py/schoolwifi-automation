<h4>1. Introduction</h4>

Selenium Python bindings provides a simple API to write functional/acceptance tests using Selenium WebDriver. Through Selenium Python API you can access all functionalities of Selenium WebDriver in an intuitive way.

Selenium Python bindings provide a convenient API to access Selenium WebDrivers like Firefox, Ie, Chrome, Remote etc. The current supported Python versions are 2.7, 3.5 and above.

<h4>2. Downloading Python bindings for Selenium and Installation</h4>

You can download Python bindings for Selenium from the <a href="https://pypi.org/project/selenium/">PyPI page for selenium package</a>. However, a better approach would be to use pip to install the selenium package. Python 3.6 has pip available in the standard library. Using pip, you can install selenium like this:

<pre><code>pip install selenium</code></pre>

<h4>3. Drivers</h4>

<p><a class="button" href="https://sites.google.com/a/chromium.org/chromedriver/downloads">download chrome driver</a></p>

Selenium requires a driver to interface with the chosen browser. Firefox, for example, requires geckodriver, which needs to be installed before the below examples can be run. Make sure it’s in your PATH, e. g., place it in /usr/bin or /usr/local/bin.

<pre><code>cp chromedriver /usr/local/bin/</code></pre>


<h4>4. Sample Selenium Snippet</h4>

create main.py file

<pre><code>
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome()
driver.get("http://www.python.org")
assert "Python" in driver.title
elem = driver.find_element_by_name("q")
elem.clear()
elem.send_keys("pycon")
elem.send_keys(Keys.RETURN)
assert "No results found." not in driver.page_source
driver.close()
</code></pre>

<h4>5. Run Script</h4>
<pre><code>python main.py</code></pre>