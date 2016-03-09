# Things To Do

* sometimes the description isn't scraped
    * try using or piped xpath | 
    ```python
        response.xpath('//*[@id="description"]').xpath('.//descendant-or-self::ul/li/text() | p/text()').extract()
    ```
