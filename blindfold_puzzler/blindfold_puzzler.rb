#! /usr/bin/env ruby

require 'yaml'
require 'pp'

if ARGV == ['seed']
	puts 'seeding puzzle database...'

	puts 'done'
	exit
end

puzzles = YAML.load_file('db.yaml')

pp puzzles.class
