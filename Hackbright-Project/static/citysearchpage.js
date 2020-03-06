"use strict"


var source = ['abu dhabi', 'adelaide', 'albuquerque', 'alexandria', 'amsterdam',
'athens', 'austin', 'baghdad', 'baltimore', 'bangkok', 'barcelona',
'beijing', 'berlin', 'birmingham', 'boston', 'brisbane', 'bristol',
'brooklyn', 'brussels', 'budapest', 'buenos aires', 'busan', 'cairo',
'calgary', 'cancun', 'cape town', 'casablanca', 'charlotte', 'chengdu',
'chennai', 'chiba', 'chicago', 'chongqing', 'colombo', 'columbus',
'copenhagen', 'cozumel', 'da nang', 'dakar', 'dalian', 'dallas',
'delhi', 'denpasar', 'denver', 'detroit', 'dhaka', 'dubai', 'dublin',
'edmonton', 'el paso', 'fort worth', 'genoa', 'giza', 'gold coast',
'guangzhou', 'guatemala city', 'guilin', 'hanoi', 'havana',
'hiroshima', 'ho chi minh city', 'hong kong', 'houston', 'hyderabad',
'incheon', 'indianapolis', 'islamabad', 'istanbul', 'jacksonville',
'jaipur', 'jakarta', 'jeddah', 'jeonju', 'jerusalem', 'johannesburg',
'karachi', 'kathmandu', 'kawasaki', 'kingston', 'kobe', 'kyoto',
'lagos', 'las vegas', 'leicester', 'lijiang', 'lima', 'lisbon',
'liverpool', 'london', 'los angeles', 'macau', 'madrid', 'malang',
'mandalay', 'manhattan', 'manila', 'mecca', 'melbourne', 'memphis',
'mexico city', 'milan', 'monterey', 'montreal', 'moscow', 'mumbai',
'munich', 'muscat', 'nanjing', 'napa', 'naples', 'nashville',
'new york city', 'nottingham', 'odessa', 'oklahoma city', 'osaka',
'oslo', 'ottawa', 'padang', 'paris', 'perth', 'philadelphia', 'phoenix',
'port elizabeth', 'port-au-prince', 'portland', 'prague', 'pyongyang',
'qingdao', 'quebec', 'queens', 'queenstown', 'reno', 'rio de janeiro',
'rome', 'saint petersburg', 'salvador', 'san diego', 'san francisco',
'san jose', 'sao paulo', 'sapporo', 'seattle', 'seoul', 'shanghai',
'shenzhen', 'singapore', 'stockholm', 'sydney', 'tainan', 'taipei',
'tangshan', 'tianjin', 'tijuana', 'tokyo', 'toronto', 'tucson', 'tunis',
'vancouver', 'vienna', 'warsaw', 'washington dc', 'wellington',
'winnipeg', 'wuhan', 'xian', 'yokohama'];


$("input#city").autocomplete({
    source: source,
    select: function(event, ui) {
        $("#submit").removeAttr("disabled");
    }
}).keyup(function() {
    var $parentContext = $(this);
    var matches = $.grep(source, function(n, i) {
        return $parentContext.val().toLowerCase() == n.toLowerCase();
    });
    $("#submit").attr("disabled", !matches.length);
});
