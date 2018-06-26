#!/usr/bin/perl

use strict;

my($line);

my($time_ms);
my($tweet);
my($sentiment);

while( defined($line = <STDIN>) )
{
  # Filter
  next if ($line =~ /^\'[0-9]+,\'/);

  chomp($line);

  #print("$line\n");

  #if ( $line =~ /([0-9]+)$/ )
  #if ( $line =~ /([-+]*?[0-9]+\.[0-9]+)$/ ) # match sentiment; $1
  #if ( $line =~ /(,)(\s+[-+]*?[0-9]+\.[0-9]+)$/ ) # match sentiment; $2
  #if ( $line =~ /(\')(,)(\s+[-+]*?[0-9]+\.[0-9]+)$/ ) # match sentiment; $3
  #if ( $line =~ /\s+(\'.+\')(,)(\s+[-+]*?[0-9]+\.[0-9]+)$/ ) # match sentiment ($3), match tweet($1)
  #if ( $line =~ /^(\'[0-9]+\')(,\s+)(\'.+\')(,)(\s+[-+]*?[0-9]+\.[0-9]+)$/ ) # match time_ms ($1), sentiment ($3), match tweet($1)
  if ( $line =~ /^(\'[0-9]+\')(,\s+)(\'.+\')(,\s+)([-+]*?[0-9]+\.[0-9]+)$/ ) # match time_ms ($1), sentiment ($3), match tweet($1)
  { 
    $sentiment = $5;
    $tweet     = $3;
    $time_ms   = $1;
  }
  else 
  {
    # Skip lines without sentinment values.
    $sentiment  = "sentiment_not_available";
    $tweet      = "sentiment_not_available";
    $time_ms    = "sentiment_not_available";;
    next;
  }

  #print("Sentiment: $sentiment\n");
  #print("Tweet    : $tweet\n");
  #print("Time (ms): $time_ms\n");

  #print("Old: $line\n");
  #print("New: $time_ms,$tweet,$sentiment\n");

  #$sentiment =~ s/\s+//g;
  ##print("$time_ms,$tweet,$sentiment\n");
  #print("$time_ms,$tweet,\'$sentiment\'\n");

  $time_ms =~ s/\'//g;    # remove single quotes
  $sentiment =~ s/\s+//g; # remove spaces
  print("$time_ms,$tweet,$sentiment\n");
}
