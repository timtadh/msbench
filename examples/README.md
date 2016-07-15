# Setup

    $ cd .../msbench/examples
    $ source .activate


## Building the Examples

    $ go install msbench/html-ex

The html-ex program is built and then placed in `msbench/examples/bin/html-ex`.
You can also control where the binary is placed using the following command

    $ go build -o <output-path> msbench/html-ex

## Running `html-ex`

    html-ex [-p <cpu-profile-path>] [-l <int>] [<input-path>]+

    Option Flags
        -h,--help                         Show this message
        -p,--cpu-profile=<path>           Path to write the cpu-profile
        -l,--loops=<int>                  Number of times to parse each input


Example:

    $ html-ex -p /tmp/html.pprof -l 100 /tmp/case.html

Running a binary not in the $PATH

    $ ./bin/html-ex -p /tmp/html.pprof -l 100 /tmp/case.html

## Changing the version

The library that does the parsing is `golang.org/x/net/html`. It is stored in
the `golang.org/x/net` repository which is checked out to
`src/golang.org/x/net`.

### Get a list of applicable versions

    $ git -C src/golang.org/x/net/ log --format=oneline | grep html | cut -d " " -f 1
    f1d3149ecb40ffadf4a28d39a30f9a125fe57bdf
    0ab009005dc16437045369e823a35d1af6232b69
    68a055e15f0ce90989da5564fd947fb72ce67513
    9b9d6d8d1165166f4dd21dcf9521215a65a4316d
    d28a91ad269180318493156412990f060d721258
    72b0708b72ac7a531f8e89f370e6214aad23ee2e
    05bc443e7e516b9767f6220284d75e2e2a704c1a
    edab5dc4135de5654f365c8062bf990097b9d903
    e0403b4e005737430c05a57aac078479844f919c
    6460565bec1e8891e29ff478184c71b9e443ac36
    3d87fd621ca9a824c5cff17216ce44769456cb3f
    ec18079348e79eb393866e87d402a1a8cc580d7f
    ccf541d87671e576d54057f6ddfa452f4cc818ea
    716c3ccf9b461e5ee71005649e4e98fdacf72d69
    5755bc4e75b2697c598004f246158b1a5bda77a7
    4109fccea424c486ca00a51bbe2ac2940e66075b
    4698117464dcc63f427cf0db12cb5b5c5e7c5bd6
    384e4d292e0c5ec2dc57cc8667ae72e907599ee9
    480e7b06ec3c006363895251ece1bf25d2386ede
    3f04d1ffd7388fb527b9688ad9d11403b7ede718
    74213743f3b1f2d57aa89df4b6669ddff7bc0bb3
    7eb0b7e953de882ffc7bf83e77c0754289edb137
    e2719b310353bccd8d4f011ff9f24e21c8812b25
    e8489d83dda556ca026a92adb0707f405d4ef8db
    46c4a49ebb6937397b4f1b78002a1156ea261f2e
    3651a440a70063fcb7028c5f214b0ffb20b3770d
    ea127e889c282c359240e0648968fbcc8b66655b


### Checkout a specific library version

    $ git -C src/golang.org/x/net/ checkout d28a91ad269180318493156412990f060d721258
    Note: checking out 'd28a91ad269180318493156412990f060d721258'.

    You are in 'detached HEAD' state. You can look around, make experimental
    changes and commit them, and you can discard any commits you make in this
    state without impacting any branches by performing another checkout.

    If you want to create a new branch to retain commits you create, you may
    do so (now or later) by using -b with the checkout command again. Example:

      git checkout -b new_branch_name

    HEAD is now at d28a91a... html/charset: use x/text/encoding/htmlindex

### Building a specific version and storing the binary

    $ mkdir html-ex-versions
    $ go build -o html-ex-versions/html-ex-d28a91ad269180318493156412990f060d721258 msbench/html-ex

### Building all versions

    $ for version in $(git -C src/golang.org/x/net/ log --format=oneline | grep html | cut -d " " -f 1); do
    >   git -C src/golang.org/x/net/ checkout $version && go build -o html-ex-versions/html-ex-$version msbench/html-ex
    > done

Note not all versions are buildable do to some package name changes. At the end
you should have the following versions

    $ ls html-ex-versions/
    html-ex-05bc443e7e516b9767f6220284d75e2e2a704c1a
    html-ex-72b0708b72ac7a531f8e89f370e6214aad23ee2e
    html-ex-ec18079348e79eb393866e87d402a1a8cc580d7f
    html-ex-3d87fd621ca9a824c5cff17216ce44769456cb3f
    html-ex-ccf541d87671e576d54057f6ddfa452f4cc818ea
    html-ex-edab5dc4135de5654f365c8062bf990097b9d903
    html-ex-6460565bec1e8891e29ff478184c71b9e443ac36
    html-ex-d28a91ad269180318493156412990f060d721258
    html-ex-716c3ccf9b461e5ee71005649e4e98fdacf72d69
    html-ex-e0403b4e005737430c05a57aac078479844f919c

You can run them like so:

    $ ./html-ex-versions/html-ex-05bc443e7e516b9767f6220284d75e2e2a704c1a 
    Please supply at least one input
    ./html-ex-versions/html-ex-05bc443e7e516b9767f6220284d75e2e2a704c1a [-p <cpu-profile-path>] [-l <int>] [<input-path>]+

    Option Flags
        -h,--help                         Show this message
        -p,--cpu-profile=<path>           Path to write the cpu-profile
        -l,--loops=<int>                  Number of times to parse each input

