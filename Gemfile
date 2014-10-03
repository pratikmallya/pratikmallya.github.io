source 'https://rubygems.org'
ruby '2.0.0'

# get the correct github pages gem
# http://jekyllrb.com/docs/github-pages/
require 'json'
require 'open-uri'
versions = JSON.parse(open('https://pages.github.com/versions.json').read)

gem 'github-pages', versions['github-pages']