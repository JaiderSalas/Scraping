from bs4 import BeautifulSoup
import json
import urllib.request
import cssutils
import logging

def Scraping(baseurl):

    cssutils.log.setLevel(logging.CRITICAL)

    opener = urllib.request.build_opener()

    opener.addheaders = [('User-Agent', 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/24 Safari/537.11'),
                            ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'),
                            ('Connection', 'keep-alive')
                        ]
    
    urllib.request.install_opener(opener)
    html_doc = urllib.request.urlopen(baseurl).read()
    
    try:
        soup = BeautifulSoup(html_doc, 'html.parser')
        for script in soup.find_all('script'):
            script.decompose()
        
        styles = {}
        for style_tag in soup.find_all('style'):
            css = cssutils.parseString(style_tag.string)
            for rule in css:
                if rule.type == rule.STYLE_RULE:
                    selector = rule.selectorText
                    if selector not in styles:
                        styles[selector] = {}
                    for prop in rule.style: 
                        styles[selector][prop.name] = prop.value
                        
        all_styles = {}
        merged_styles = {}
        
        for tag in soup.find_all(True):
            tag_styles = {}
            if tag.name in styles:
                tag_styles |= styles[tag.name]
                
            if 'class' in tag.attrs:
                for class_name in tag['class']:
                    if f'.{class_name}' in styles:
                        tag_styles |= styles[f'.{class_name}']
                        
            if tag.get('id') and '#' + tag['id'] in styles:
                tag_styles |= styles['#' + tag['id']]

            if 'style' in tag.attrs:
                inline_styles = cssutils.parseString(tag['style'])
                tag_styles |= {prop.name: prop.value for prop in inline_styles}
                
            all_styles[tag] = tag_styles
            style_str = str(tag_styles)

            if style_str not in merged_styles:
                merged_styles[style_str] = []
            merged_styles[style_str].append(tag)


        
    except Exception as e:
        print ("Exception occurred = ",e)
    
    styles_by_tags = {}
    for style_str, tags in merged_styles.items():
        for tag in tags:
            if tag.name not in styles_by_tags:
                styles_by_tags[tag.name] = {}
            if style_str != '{}':
                styles_by_tags[tag.name].update(eval(style_str))
                
    return styles_by_tags

def print_styles(styles_by_tag):
    for tag_name, styles in styles_by_tag.items():
        if not styles:
            continue
        print(f"Etiqueta: {tag_name}")
        print(f"Estilos: {styles}")
        print("-" * 20)

def main():
    all_styles = {}
    URLS = [
        "https://www.google.com",
        "https://www.instagram.com",
        "https://www.youtube.com",
        "https://www.twitter.com",
        "https://www.linkedin.com",
        "https://www.netflix.com",
        "https://www.spotify.com",
        "https://www.amazon.com",
        "https://www.ebay.com",
        "https://www.apple.com",
        "https://www.microsoft.com",
        "https://www.wikipedia.org",
        "https://www.wordpress.org",
        "https://www.blogger.com",
        "https://www.w3schools.com",
        "https://www.stackoverflow.com",
        "https://www.github.com",
        "https://www.gitlab.com",
        "https://www.bitbucket.org",
        "https://www.heroku.com",
        "https://www.digitalocean.com",
        "https://www.ibm.com",
        "https://www.nvidia.com",
        "https://www.samsung.com",
        "https://www.lg.com",
        "https://www.philips.com",
        "https://www.nokia.com",
        "https://www.xiaomi.com",
        "https://www.oneplus.com",
        "https://www.asus.com",
        "https://www.lenovo.com",
        "https://www.hp.com",
        "https://co.computrabajo.com"
    ]
    for url in URLS:
        print(f"Scraping {url}")
        styles = Scraping(url)
        if styles:
            all_styles[url] = styles
        else: continue
    with open('data.json', 'w') as file:
        json.dump(all_styles, file, indent=4)
    
    
    
main()