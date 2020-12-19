## Config.ini 應有下面項目
```
    [LINE]
    Token = <你的LINE token>

    [Targets]
    Target1 = drug use hiv infection and harm reduction
    Target2 = drug-use-hiv-infection-and-harm-reduction
    Target3 = drug use, hiv infection, and harm reduction

    [Searching]
    Search1 = drug+use+hiv+infection+and+harm+reduction
    Search2 = drug-use-hiv-infection-and-harm-reduction

    [Sites]
    Site1 = Google
    Site2 = Yahoo
    Site3 = Bing

    [Google]
    url = https://www.google.com.tw/search?q=
    Looking word = div#rso div.g
    Looking Raw = 0

    [Yahoo]
    url = https://tw.search.yahoo.com/search?p=
    Looking word = div#main div#web ol li
    Looking Raw = 0

    [Bing]
    url = https://www.bing.com/search?q=
    Looking word = li.b_algo
    Looking Raw = 1

    [EXCLUDE SITE]
    1 = aids-stop.com
```
