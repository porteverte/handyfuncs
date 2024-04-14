**handyfuncs | handy functions for manipulating data and automating processes**

<h1>About</h1>

This functions in this package include but are not not limited to:

**Data Manipulation**

1. Merge Dictrionaries
2. Convert Dictionary to List
3. Get Initials
4. Number of Words in String

**Automation**

1. Write to Log
2. Run Subprocess
3. Current Method Name
4. Execute Function

<h1>Data Manipulation</h>
    
<h2>Merge Dictionaries</h2>

This will not only merge the items in each dictionary but also merge the items in any shared lists

    from handyfuncs import merge_dictionaries
    
    d1 = {
          'clothes': ['shoes', 'socks', 'ties']
          , 'food': ['cheese', 'bananas', 'lentils']
          }
    d2 = {
          'clothes': ['shoes', 'socks', 'shorts', 'hats']
          , 'cutlery': ['knives', 'forks']
          }
    d3 = merge_dictionaries(d1, d2)

<h1>Disclaimer</h1>

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.