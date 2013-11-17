#!/usr/bin/perl
use 5.12.0;
use warnings FATAL => 'all';

our $URL = "http://www.fogcloud.org/cgi-bin/fakedht.cgi";
our $KEY = shift;
our $VFN = shift;

die "Usage: ./$0 key file" unless ($KEY && $VFN);

open my $file, "<", $VFN or die "Error opening $VFN: $!";
close $file;

use LWP::UserAgent;
my $ua = LWP::UserAgent->new;

my $res = $ua->post(
    $URL,
    Content_Type => 'form-data',
    Content => [
        key  => $KEY,
        data => [$VFN]
    ],
);

say $res->status_line;
say $res->content;
