#!/usr/bin/perl
use 5.12.0;
use warnings FATAL => 'all';

our $URL = "http://www.fogcloud.org/cgi-bin/fakedht.cgi";
our $KEY = shift or die "Usage: ./$0 key";

use LWP::UserAgent;
my $ua = LWP::UserAgent->new;

my $req = HTTP::Request->new(GET => "$URL?key=$KEY");
my $res = $ua->request($req);

say $res->status_line;
say $res->content;
