/*
A KBase module: kb_bakta
*/

module kb_bakta {
    typedef structure {
        string report_name;
        string report_ref;
    } ReportResults;

    /*
        This example function accepts any number of parameters and returns results in a KBaseReport
    */
    funcdef run_kb_bakta(mapping<string,UnspecifiedObject> params) returns (ReportResults output) authentication required;

    funcdef annotate_proteins(mapping<string,string> proteins) returns (mapping<string,UnspecifiedObject>) authentication required;
};
