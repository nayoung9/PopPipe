#!/usr/bin/perl

#####
#  Usage 	
#  $./STRUCTURE.pl -p [parameter file] -o [out directory]
#
#  Input
#	Parameter file
#
#  Output
#	structure png file
#
#  Information
#	Made by	Youngbeen and Jongin
#	2018.05.25
#	Update by NY
#	2021. 01.
#  	
#####

use strict;
use warnings;
use Getopt::Long qw(:config no_ignore_case);
use File::Basename;
use Cwd 'abs_path';
use Parallel::ForkManager;
use FindBin '$Bin';
use Sort::Key::Natural 'natsort';
use Switch;

## Parameters
my $param_f;
my $sparam_f;
my $outdir = "./";
my $core = 1;
my $help = 0;

GetOptions(
	"param|p=s"   => \$param_f,
	"sample|s=s"   => \$sparam_f,
	"threads|t=i" => \$core,
	"outdir|o=s"  => \$outdir,
	"help|h"      => \$help,
);

if ($help == 1 || !$param_f) {
	print STDERR "usage:\n\$./STRUCTURE.pl -p PARAM -s SAMPLE_PARAM -n NAME -o OUT_DIR \n\n";
	print STDERR "optional arguments:\n";
	print STDERR "\t-h, --help\tshow tihis help message and exit\n";
	print STDERR "\t-p, --param\tPARAM\n\t\t\t<Path> parameter file\n";
	print STDERR "\t-s, --sample\tSAMPLE_PARAM\n\t\t\t<Path> sample parameter file\n";
	print STDERR "\t-t, --threads\tTHREADS\n\t\t\t<Path> # of threads\n";
	print STDERR "\t-o, --outdir\tOUT_DIR\n\t\t\t<Path> Output directory\n";
	print STDERR "\n================================================\n\n";
	exit;
}
my $filename = "Structure_result";

### Configure parameters
my $admixture = "";
my $CLUMPAK = "";
my $bed = "";
my $k = "";
my $color = "";
my $Using_color = 0;
my $pop = "";
$outdir = abs_path($outdir);
`mkdir -p $outdir`;

open(W2, ">$outdir/$filename.color");
open(PARAM,$param_f);
while(<PARAM>){
	chomp;
	if($_ =~ /^#/ || $_ eq ""){next;}
	my @p = split(/\s*=\s*/);
	if($p[0] =~ /Color(\d+)/ ) {
		print W2 "$1 $p[1]\n";
		$Using_color++;
		next;
	}
	switch ($p[0]) {
		case("admixture")	{ $admixture = abs_path($p[1]); }
		case("CLUMPAK")		{ $CLUMPAK = abs_path($p[1]); }
		case("bed")		{ $bed = abs_path($p[1]); }
		case("k")		{ $k = int($p[1]); }
	}

}
if ( $Using_color == 0 ) {
	print W2 "Using default color file\n";
}
close(PARAM);

open(SPARAM, $sparam_f);
open(W1, ">$outdir/$filename.pop");
while(<SPARAM>){
	chomp;
	$_ =~ s/^\s+|\s+$//g;
	if($_ =~ /^#/ || $_ eq ""){next;}

	my @p = split(/\s+/,$_);
	print W1 "$p[2]\n";
}
close(W1);
close(SPARAM);


close(W2);
close(W1);
$pop = "$outdir/$filename.pop";
$color = "$outdir/$filename.color";


$admixture =~ s/ //g;
$CLUMPAK =~ s/ //g;
$bed =~ s/ //g;

chdir($outdir);
my @cmds = ();
for ( my $pi = 2; $pi <= $k ; $pi++ ) {
	my $cmd = "$admixture $bed $pi --cv -B > $pi.log  2>&1";
	push(@cmds,$cmd);
}


### population structure analysis using admixture
my $pm = new Parallel::ForkManager($core);
for (my $i = 0; $i <= $#cmds ; $i++) {
	sleep(1);
	$pm->start and next;
	print STDERR "Running: $cmds[$i]\n";
	`$cmds[$i]`;
	$pm->finish
}
$pm->wait_all_children;
my @split = split(/\//, $bed);
$bed = substr $split[$#split], 0, -4;

`zip $outdir/$filename.clumpak.zip $outdir/*.Q`;

if ( $Using_color == 0 ) { 
	`perl $CLUMPAK --id 100 --dir $outdir/CLUMPAK --file $outdir/$filename.clumpak.zip --inputtype admixture --indtopop $pop`;
} else {	
	`perl $CLUMPAK --id 100 --dir $outdir/CLUMPAK --file $outdir/$filename.clumpak.zip --inputtype admixture --indtopop $pop --colors $color`;
}


