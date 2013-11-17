#!/usr/bin/perl
use 5.12.0;
use warnings FATAL => 'all';

our $DATA = "/var/tmp/fakedht";

system(qq{mkdir -p "$DATA"});
system(qq(find "$DATA" -name "*.cfg" -mtime +1 -exec rm {} \\;));

use CGI;
use IO::Handle;
use Data::Dumper;

my $qq = CGI->new;

sub fail {
    my ($msg) = @_;
    print $qq->header(-status => "500 $msg", -type   => "text/plain");
    print "Error handling request:\n";
    print "$msg\n";
    exit(0);
}

sub get_record {
    my $key = $qq->param('key');
    fail("Bad key") unless($key =~ /^\w+$/);

    open my $file, "<", "$DATA/$key.cfg"
      or fail("No such key");

    print $qq->header(-type => "application/octet-stream");

    my $temp;
    while (read $file, $temp, 4096) {
        print $temp;
    }

    close($file);

    exit(0);
}

sub put_record {
    my $key = $qq->param('key');
    fail("Bad key") unless($key =~ /^\w+$/);

    my $up = $qq->upload('data');

    my $data = "";
    my $temp;
    while (read $up, $temp, 4096) {
        $data .= $temp;
        fail("Data too big") if(length($data) > 65536);
    }

    open my $out, ">", "$DATA/$key.cfg"
      or fail("IO Error");
   
    $out->print($data);
   
    close $out;

    
    print $qq->header(-type => "text/plain");
    print "ok\n";

    exit(0);
}

if ($qq->request_method() eq 'GET') {
    get_record();
}

if ($qq->request_method() eq 'POST') {
    put_record();
}

fail("Bad request method: " . $qq->request_method());
