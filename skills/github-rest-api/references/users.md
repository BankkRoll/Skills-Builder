# REST API endpoints for artifact attestations and more

# REST API endpoints for artifact attestations

> Use the REST API to manage artifact attestations.

## List attestations by bulk subject digests

List a collection of artifact attestations associated with any entry in a list of subject digests owned by a user.

The collection of attestations returned by this endpoint is filtered according to the authenticated user's permissions; if the authenticated user cannot read a repository, the attestations associated with that repository will not be included in the response. In addition, when using a fine-grained access token the `attestations:read` permission is required.

**Please note:** in order to offer meaningful security benefits, an attestation's signature and timestamps **must** be cryptographically verified, and the identity of the attestation signer **must** be validated. Attestations can be verified using the [GitHub CLIattestation verifycommand](https://cli.github.com/manual/gh_attestation_verify). For more information, see [our guide on how to use artifact attestations to establish a build's provenance](https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds).

### Fine-grained access tokens for "List attestations by bulk subject digests"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List attestations by bulk subject digests"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |

| Name, Type, Description |
| --- |
| subject_digestsarray of stringsRequiredList of subject digests to fetch attestations for. |
| predicate_typestringOptional filter for fetching attestations with a given predicate type.
This option acceptsprovenance,sbom,release, or freeform text
for custom predicate types. |

### HTTP response status codes for "List attestations by bulk subject digests"

| Status code | Description |
| --- | --- |
| 200 | OK |

### Code samples for "List attestations by bulk subject digests"

#### Request example

post/users/{username}/attestations/bulk-list

-
-
-

`curl -L \
  -X POST \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/attestations/bulk-list \
  -d '{"subject_digests":["sha256:abc123","sha512:def456"]}'`

Response

-
-

`Status: 200``{
"attestations_subject_digests": [
{
"sha256:abc": [
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
},
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
}
]
}
]
}`

## Delete attestations in bulk

Delete artifact attestations in bulk by either subject digests or unique ID.

### Fine-grained access tokens for "Delete attestations in bulk"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (write)

### Parameters for "Delete attestations in bulk"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| subject_digestsarray of stringsRequiredList of subject digests associated with the artifact attestations to delete. |

### HTTP response status codes for "Delete attestations in bulk"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

## Delete attestations by subject digest

Delete an artifact attestation by subject digest.

### Fine-grained access tokens for "Delete attestations by subject digest"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (write)

### Parameters for "Delete attestations by subject digest"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |
| subject_digeststringRequiredSubject Digest |

### HTTP response status codes for "Delete attestations by subject digest"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "Delete attestations by subject digest"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 204delete/users/{username}/attestations/digest/{subject_digest}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/attestations/digest/SUBJECT_DIGEST`

Response

`Status: 200`

## Delete attestations by ID

Delete an artifact attestation by unique ID that is associated with a repository owned by a user.

### Fine-grained access tokens for "Delete attestations by ID"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Attestations" repository permissions (write)

### Parameters for "Delete attestations by ID"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |
| attestation_idintegerRequiredAttestation ID |

### HTTP response status codes for "Delete attestations by ID"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 204 | No Content |
| 403 | Forbidden |
| 404 | Resource not found |

### Code samples for "Delete attestations by ID"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 204delete/users/{username}/attestations/{attestation_id}

-
-
-

`curl -L \
  -X DELETE \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/attestations/ATTESTATION_ID`

Response

`Status: 200`

## List attestations

List a collection of artifact attestations with a given subject digest that are associated with repositories owned by a user.

The collection of attestations returned by this endpoint is filtered according to the authenticated user's permissions; if the authenticated user cannot read a repository, the attestations associated with that repository will not be included in the response. In addition, when using a fine-grained access token the `attestations:read` permission is required.

**Please note:** in order to offer meaningful security benefits, an attestation's signature and timestamps **must** be cryptographically verified, and the identity of the attestation signer **must** be validated. Attestations can be verified using the [GitHub CLIattestation verifycommand](https://cli.github.com/manual/gh_attestation_verify). For more information, see [our guide on how to use artifact attestations to establish a build's provenance](https://docs.github.com/actions/security-guides/using-artifact-attestations-to-establish-provenance-for-builds).

### Fine-grained access tokens for "List attestations"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List attestations"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |
| subject_digeststringRequiredSubject Digest |

| Name, Type, Description |
| --- |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |
| beforestringA cursor, as given in theLink header. If specified, the query only searches for results before this cursor. For more information, see "Using pagination in the REST API." |
| afterstringA cursor, as given in theLink header. If specified, the query only searches for results after this cursor. For more information, see "Using pagination in the REST API." |
| predicate_typestringOptional filter for fetching attestations with a given predicate type.
This option acceptsprovenance,sbom,release, or freeform text
for custom predicate types. |

### HTTP response status codes for "List attestations"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 201 | Created |
| 204 | No Content |
| 404 | Resource not found |

### Code samples for "List attestations"

#### Request example

get/users/{username}/attestations/{subject_digest}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/attestations/SUBJECT_DIGEST`

Response

-
-

`Status: 200``{
"attestations": [
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
},
{
"bundle": {
"mediaType": "application/vnd.dev.sigstore.bundle.v0.3+json",
"verificationMaterial": {
"tlogEntries": [
{
"logIndex": "97913980",
"logId": {
"keyId": "wNI9atQGlz+VWfO6LRygH4QUfY/8W4RFwiT5i5WRgB0="
},
"kindVersion": {
"kind": "dsse",
"version": "0.0.1"
},
"integratedTime": "1716998992",
"inclusionPromise": {
"signedEntryTimestamp": "MEYCIQCeEsQAy+qXtULkh52wbnHrkt2R2JQ05P9STK/xmdpQ2AIhANiG5Gw6cQiMnwvUz1+9UKtG/vlC8dduq07wsFOViwSL"
},
"inclusionProof": {
"logIndex": "93750549",
"rootHash": "KgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=",
"treeSize": "93750551",
"hashes": [
"8LI21mzwxnUSo0fuZeFsUrz2ujZ4QAL+oGeTG+5toZg=",
"nCb369rcIytNhGwWoqBv+eV49X3ZKpo/HJGKm9V+dck=",
"hnNQ9mUdSwYCfdV21pd87NucrdRRNZATowlaRR1hJ4A=",
"MBhhK33vlD4Tq/JKgAaXUI4VjmosWKe6+7RNpQ2ncNM=",
"XKWUE3stvGV1OHsIGiCGfn047Ok6uD4mFkh7BaicaEc=",
"Tgve40VPFfuei+0nhupdGpfPPR+hPpZjxgTiDT8WNoY=",
"wV+S/7tLtYGzkLaSb6UDqexNyhMvumHK/RpTNvEZuLU=",
"uwaWufty6sn6XqO1Tb9M3Vz6sBKPu0HT36mStxJNd7s=",
"jUfeMOXQP0XF1JAnCEETVbfRKMUwCzrVUzYi8vnDMVs=",
"xQKjzJAwwdlQG/YUYBKPXxbCmhMYKo1wnv+6vDuKWhQ=",
"cX3Agx+hP66t1ZLbX/yHbfjU46/3m/VAmWyG/fhxAVc=",
"sjohk/3DQIfXTgf/5XpwtdF7yNbrf8YykOMHr1CyBYQ=",
"98enzMaC+x5oCMvIZQA5z8vu2apDMCFvE/935NfuPw8="
],
"checkpoint": {
"envelope": "rekor.sigstore.dev - 2605736670972794746\\n93750551\\nKgKiXoOl8rM5d4y6Xlbm2QLftvj/FYvTs6z7dJlNO60=\\n\\n— rekor.sigstore.dev wNI9ajBEAiBkLzdjY8A9HReU7rmtjwZ+JpSuYtEr9SmvSwUIW7FBjgIgKo+vhkW3tqc+gc8fw9gza3xLoncA8a+MTaJYCaLGA9c=\\n"
}
},
"canonicalizedBody": "eyJhcGlWZXJzaW9uIjoiMC4wLjEiLCJraW5kIjoiZHNzZSIsInNwZWMiOnsiZW52ZWxvcGVIYXNoIjp7ImFsZ29yaXRobSI6InNoYTI1NiIsInZhbHVlIjoiM2I1YzkwNDk5MGFiYzE4NjI1ZWE3Njg4MzE1OGEwZmI4MTEwMjM4MGJkNjQwZjI5OWJlMzYwZWVkOTMxNjYwYiJ9LCJwYXlsb2FkSGFzaCI6eyJhbGdvcml0aG0iOiJzaGEyNTYiLCJ2YWx1ZSI6IjM4ZGNlZDJjMzE1MGU2OTQxMDViYjZiNDNjYjY3NzBiZTYzZDdhNGM4NjNiMTc2YTkwMmU1MGQ5ZTAyN2ZiMjMifSwic2lnbmF0dXJlcyI6W3sic2lnbmF0dXJlIjoiTUVRQ0lFR0lHQW03Z1pWTExwc3JQY2puZEVqaXVjdEUyL2M5K2o5S0d2YXp6M3JsQWlBZDZPMTZUNWhrelJNM0liUlB6bSt4VDQwbU5RWnhlZmQ3bGFEUDZ4MlhMUT09IiwidmVyaWZpZXIiOiJMUzB0TFMxQ1JVZEpUaUJEUlZKVVNVWkpRMEZVUlMwdExTMHRDazFKU1VkcVZFTkRRbWhUWjBGM1NVSkJaMGxWVjFsNGNVdHpjazFUTTFOMmJEVkphalZQUkdaQ1owMUtUeTlKZDBObldVbExiMXBKZW1vd1JVRjNUWGNLVG5wRlZrMUNUVWRCTVZWRlEyaE5UV015Ykc1ak0xSjJZMjFWZFZwSFZqSk5ValIzU0VGWlJGWlJVVVJGZUZaNllWZGtlbVJIT1hsYVV6RndZbTVTYkFwamJURnNXa2RzYUdSSFZYZElhR05PVFdwUmQwNVVTVFZOVkZsM1QxUlZlVmRvWTA1TmFsRjNUbFJKTlUxVVdYaFBWRlY1VjJwQlFVMUdhM2RGZDFsSUNrdHZXa2w2YWpCRFFWRlpTVXR2V2tsNmFqQkVRVkZqUkZGblFVVmtiV2RvVGs1M00yNVZMMHQxWlZGbmMzQkhTRmMzWjJnNVdFeEVMMWRrU1RoWlRVSUtLekJ3TUZZMGJ6RnJTRzgyWTAweGMwUktaM0pEWjFCUlZYcDRjSFZaZFc4cmVIZFFTSGxzTDJ0RWVXWXpSVXhxYTJGUFEwSlVUWGRuWjFWMlRVRTBSd3BCTVZWa1JIZEZRaTkzVVVWQmQwbElaMFJCVkVKblRsWklVMVZGUkVSQlMwSm5aM0pDWjBWR1FsRmpSRUY2UVdSQ1owNVdTRkUwUlVablVWVnhaa05RQ25aWVMwRjJVelJEWkdoUk1taGlXbGRLVTA5RmRsWnZkMGgzV1VSV1VqQnFRa0puZDBadlFWVXpPVkJ3ZWpGWmEwVmFZalZ4VG1wd1MwWlhhWGhwTkZrS1drUTRkMWRuV1VSV1VqQlNRVkZJTDBKR1FYZFViMXBOWVVoU01HTklUVFpNZVRsdVlWaFNiMlJYU1hWWk1qbDBUREpPYzJGVE9XcGlSMnQyVEcxa2NBcGtSMmd4V1drNU0ySXpTbkphYlhoMlpETk5kbHBIVm5kaVJ6azFZbGRXZFdSRE5UVmlWM2hCWTIxV2JXTjVPVzlhVjBaclkzazVNR051Vm5WaGVrRTFDa0puYjNKQ1owVkZRVmxQTDAxQlJVSkNRM1J2WkVoU2QyTjZiM1pNTTFKMllUSldkVXh0Um1wa1IyeDJZbTVOZFZveWJEQmhTRlpwWkZoT2JHTnRUbllLWW01U2JHSnVVWFZaTWpsMFRVSTRSME5wYzBkQlVWRkNaemM0ZDBGUlNVVkZXR1IyWTIxMGJXSkhPVE5ZTWxKd1l6TkNhR1JIVG05TlJGbEhRMmx6UndwQlVWRkNaemM0ZDBGUlRVVkxSMXBvV2xkWmVWcEhVbXRQUkVacFRVUmplazVxWXpCUFJGRjRUVEpGTTFsNldUQk9iVTVyVFVkS2JWbDZTVEpaZWtGM0NsbFVRWGRIUVZsTFMzZFpRa0pCUjBSMmVrRkNRa0ZSUzFKSFZuZGlSemsxWWxkV2RXUkVRVlpDWjI5eVFtZEZSVUZaVHk5TlFVVkdRa0ZrYW1KSGEzWUtXVEo0Y0UxQ05FZERhWE5IUVZGUlFtYzNPSGRCVVZsRlJVaEtiRnB1VFhaaFIxWm9Xa2hOZG1SSVNqRmliWE4zVDNkWlMwdDNXVUpDUVVkRWRucEJRZ3BEUVZGMFJFTjBiMlJJVW5kamVtOTJURE5TZG1FeVZuVk1iVVpxWkVkc2RtSnVUWFZhTW13d1lVaFdhV1JZVG14amJVNTJZbTVTYkdKdVVYVlpNamwwQ2sxR2QwZERhWE5IUVZGUlFtYzNPSGRCVVd0RlZHZDRUV0ZJVWpCalNFMDJUSGs1Ym1GWVVtOWtWMGwxV1RJNWRFd3lUbk5oVXpscVlrZHJka3h0WkhBS1pFZG9NVmxwT1ROaU0wcHlXbTE0ZG1RelRYWmFSMVozWWtjNU5XSlhWblZrUXpVMVlsZDRRV050Vm0xamVUbHZXbGRHYTJONU9UQmpibFoxWVhwQk5BcENaMjl5UW1kRlJVRlpUeTlOUVVWTFFrTnZUVXRIV21oYVYxbDVXa2RTYTA5RVJtbE5SR042VG1wak1FOUVVWGhOTWtVeldYcFpNRTV0VG10TlIwcHRDbGw2U1RKWmVrRjNXVlJCZDBoUldVdExkMWxDUWtGSFJIWjZRVUpEZDFGUVJFRXhibUZZVW05a1YwbDBZVWM1ZW1SSFZtdE5RMjlIUTJselIwRlJVVUlLWnpjNGQwRlJkMFZJUVhkaFlVaFNNR05JVFRaTWVUbHVZVmhTYjJSWFNYVlpNamwwVERKT2MyRlRPV3BpUjJ0M1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWdwRVVWRnhSRU5vYlZsWFZtMU5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBGSENrTnBjMGRCVVZGQ1p6YzRkMEZSTkVWRlozZFJZMjFXYldONU9XOWFWMFpyWTNrNU1HTnVWblZoZWtGYVFtZHZja0puUlVWQldVOHZUVUZGVUVKQmMwMEtRMVJKZUUxcVdYaE5la0V3VDFSQmJVSm5iM0pDWjBWRlFWbFBMMDFCUlZGQ1FtZE5SbTFvTUdSSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhZ3BpUjJ0M1IwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWUlVVdEVRV2N4VDFSamQwNUVZM2hOVkVKalFtZHZja0puUlVWQldVOHZUVUZGVTBKRk5FMVVSMmd3Q21SSVFucFBhVGgyV2pKc01HRklWbWxNYlU1MllsTTVhbUpIYTNaWk1uaHdUSGsxYm1GWVVtOWtWMGwyWkRJNWVXRXlXbk5pTTJSNlRESlNiR05IZUhZS1pWY3hiR0p1VVhWbFZ6RnpVVWhLYkZwdVRYWmhSMVpvV2toTmRtUklTakZpYlhOM1QwRlpTMHQzV1VKQ1FVZEVkbnBCUWtWM1VYRkVRMmh0V1ZkV2JRcE5iVkpyV2tSbmVGbHFRVE5OZWxrelRrUm5NRTFVVG1oT01rMHlUa1JhYWxwRVFtbGFiVTE1VG0xTmQwMUhSWGROUTBWSFEybHpSMEZSVVVKbk56aDNDa0ZTVVVWRmQzZFNaREk1ZVdFeVduTmlNMlJtV2tkc2VtTkhSakJaTW1kM1ZGRlpTMHQzV1VKQ1FVZEVkbnBCUWtaUlVTOUVSREZ2WkVoU2QyTjZiM1lLVERKa2NHUkhhREZaYVRWcVlqSXdkbGt5ZUhCTU1rNXpZVk01YUZrelVuQmlNalY2VEROS01XSnVUWFpQVkVrMFQxUkJNMDVVWXpGTmFUbG9aRWhTYkFwaVdFSXdZM2s0ZUUxQ1dVZERhWE5IUVZGUlFtYzNPSGRCVWxsRlEwRjNSMk5JVm1saVIyeHFUVWxIVEVKbmIzSkNaMFZGUVdSYU5VRm5VVU5DU0RCRkNtVjNRalZCU0dOQk0xUXdkMkZ6WWtoRlZFcHFSMUkwWTIxWFl6TkJjVXBMV0hKcVpWQkxNeTlvTkhCNVowTTRjRGR2TkVGQlFVZFFlRkl4ZW1KblFVRUtRa0ZOUVZORVFrZEJhVVZCS3pobmJGRkplRTlCYUZoQ1FVOVRObE1yT0ZweGQwcGpaSGQzVTNJdlZGZHBhSE16WkV4eFZrRjJiME5KVVVSaWVUbG9NUXBKWTNWRVJYSXJlbk5YYVV3NFVIYzFRMU5VZEd0c2RFbzBNakZ6UlRneFZuWjFOa0Z3VkVGTFFtZG5jV2hyYWs5UVVWRkVRWGRPYmtGRVFtdEJha0VyQ2tSSU4xQXJhR2cwVmtoWFprTlhXSFJ5UzFSdlFrdDFZa0pyUzNCbVYwTlpVWGhxV0UweWRsWXZibEJ4WWxwR1dVOVdXazlpWlRaQlRuSm5lV1J2V1VNS1RVWlZUV0l6ZUhwelJrNVJXWFp6UlZsUGFUSkxibkoyUmpCMFoyOXdiVmhIVm05NmJsb3JjUzh5UVVsRVZ6bEdNVVUzV1RaWk1EWXhaVzkxUVZsa1NBcFhkejA5Q2kwdExTMHRSVTVFSUVORlVsUkpSa2xEUVZSRkxTMHRMUzBLIn1dfX0="
}
],
"timestampVerificationData": {},
"certificate": {
"rawBytes": "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"
}
},
"dsseEnvelope": {
"payload": "eyJfdHlwZSI6Imh0dHBzOi8vaW4tdG90by5pby9TdGF0ZW1lbnQvdjEiLCJzdWJqZWN0IjpbeyJuYW1lIjoiZ2hfMi41MC4wX3dpbmRvd3NfYXJtNjQuemlwIiwiZGlnZXN0Ijp7InNoYTI1NiI6IjhhYWQxMjBiNDE2Mzg2YjQyNjllZjYyYzhmZGViY2FkMzFhNzA4NDcyOTc4MTdhMTQ5ZGFmOTI3ZWRjODU1NDgifX1dLCJwcmVkaWNhdGVUeXBlIjoiaHR0cHM6Ly9zbHNhLmRldi9wcm92ZW5hbmNlL3YxIiwicHJlZGljYXRlIjp7ImJ1aWxkRGVmaW5pdGlvbiI6eyJidWlsZFR5cGUiOiJodHRwczovL3Nsc2EtZnJhbWV3b3JrLmdpdGh1Yi5pby9naXRodWItYWN0aW9ucy1idWlsZHR5cGVzL3dvcmtmbG93L3YxIiwiZXh0ZXJuYWxQYXJhbWV0ZXJzIjp7IndvcmtmbG93Ijp7InJlZiI6InJlZnMvaGVhZHMvdHJ1bmsiLCJyZXBvc2l0b3J5IjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkiLCJwYXRoIjoiLmdpdGh1Yi93b3JrZmxvd3MvZGVwbG95bWVudC55bWwifX0sImludGVybmFsUGFyYW1ldGVycyI6eyJnaXRodWIiOnsiZXZlbnRfbmFtZSI6IndvcmtmbG93X2Rpc3BhdGNoIiwicmVwb3NpdG9yeV9pZCI6IjIxMjYxMzA0OSIsInJlcG9zaXRvcnlfb3duZXJfaWQiOiI1OTcwNDcxMSJ9fSwicmVzb2x2ZWREZXBlbmRlbmNpZXMiOlt7InVyaSI6ImdpdCtodHRwczovL2dpdGh1Yi5jb20vY2xpL2NsaUByZWZzL2hlYWRzL3RydW5rIiwiZGlnZXN0Ijp7ImdpdENvbW1pdCI6ImZhZWYyZGRkODFiMDczNjc0ODQxM2E3YzY0NmNkMGJmYzI2YzAwYTAifX1dfSwicnVuRGV0YWlscyI6eyJidWlsZGVyIjp7ImlkIjoiaHR0cHM6Ly9naXRodWIuY29tL2FjdGlvbnMvcnVubmVyL2dpdGh1Yi1ob3N0ZWQifSwibWV0YWRhdGEiOnsiaW52b2NhdGlvbklkIjoiaHR0cHM6Ly9naXRodWIuY29tL2NsaS9jbGkvYWN0aW9ucy9ydW5zLzkyODkwNzU3NTIvYXR0ZW1wdHMvMSJ9fX19",
"payloadType": "application/vnd.in-toto+json",
"signatures": [
{
"sig": "MEQCIEGIGAm7gZVLLpsrPcjndEjiuctE2/c9+j9KGvazz3rlAiAd6O16T5hkzRM3IbRPzm+xT40mNQZxefd7laDP6x2XLQ=="
}
]
}
},
"repository_id": 1
}
]
}`

---

# REST API endpoints for blocking users

> Use the REST API to manage blocked users.

## About blocking users

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for emails

> Use the REST API to manage email addresses of authenticated users.

## About email administration

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for followers

> Use the REST API to get information about followers of authenticated users.

## About follower administration

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for GPG keys

> Use the REST API to manage GPG keys of authenticated users.

## About user GPG key administration

The data returned in the `public_key` response field is not a GPG formatted key. When a user uploads a GPG key, it is parsed and the cryptographic public key is extracted and stored. This cryptographic key is what the endpoints in this category will return. This key is not suitable for direct use in programs such as GPG.

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for Git SSH keys

> Use the REST API to manage Git SSH keys of authenticated users.

## About Git SSH key administration

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for social accounts

> Use the REST API to manage social accounts of authenticated users.

## About social account administration

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for SSH signing keys

> Use the REST API to manage SSH signing keys of authenticated users.

## About SSH signing key administration

If a request URL does not include a `{username}` parameter then the response will be for the signed-in user (and you must pass [authentication information](https://docs.github.com/en/rest/overview/authenticating-to-the-rest-api) with your request). Additional private information, such as whether a user has two-factor authentication enabled, is included when authenticated through OAuth with the `user` scope.

---

# REST API endpoints for users

> Use the REST API to get public and private information about authenticated users.

## Get the authenticated user

OAuth app tokens and personal access tokens (classic) need the `user` scope in order for the response to include private profile information.

### Fine-grained access tokens for "Get the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

### HTTP response status codes for "Get the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |

### Code samples for "Get the authenticated user"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 200get/user

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user`

Response with public and private profile information

-
-

`Status: 200``{
"login": "octocat",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octocat",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"repos_url": "https://api.github.com/users/octocat/repos",
"events_url": "https://api.github.com/users/octocat/events{/privacy}",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": false,
"name": "monalisa octocat",
"company": "GitHub",
"blog": "https://github.com/blog",
"location": "San Francisco",
"email": "octocat@github.com",
"hireable": false,
"bio": "There once was...",
"twitter_username": "monatheoctocat",
"public_repos": 2,
"public_gists": 1,
"followers": 20,
"following": 0,
"created_at": "2008-01-14T04:33:35Z",
"updated_at": "2008-01-14T04:33:35Z",
"private_gists": 81,
"total_private_repos": 100,
"owned_private_repos": 100,
"disk_usage": 10000,
"collaborators": 8,
"two_factor_authentication": true,
"plan": {
"name": "Medium",
"space": 400,
"private_repos": 20,
"collaborators": 0
}
}`

## Update the authenticated user

**Note:** If your email is set to private and you send an `email` parameter as part of this request to update your profile, your privacy settings are still enforced: the email address will not be displayed on your public profile or via the API.

### Fine-grained access tokens for "Update the authenticated user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token must have the following permission set:

- "Profile" user permissions (write)

### Parameters for "Update the authenticated user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| namestringThe new name of the user. |
| emailstringThe publicly visible email address of the user. |
| blogstringThe new blog URL of the user. |
| twitter_usernamestring or nullThe new Twitter username of the user. |
| companystringThe new company of the user. |
| locationstringThe new location of the user. |
| hireablebooleanThe new hiring availability of the user. |
| biostringThe new short biography of the user. |

### HTTP response status codes for "Update the authenticated user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |
| 401 | Requires authentication |
| 403 | Forbidden |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Update the authenticated user"

#### Request example

patch/user

-
-
-

`curl -L \
  -X PATCH \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user \
  -d '{"blog":"https://github.com/blog","name":"monalisa octocat"}'`

Response

-
-

`Status: 200``{
"login": "octocat",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octocat",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"repos_url": "https://api.github.com/users/octocat/repos",
"events_url": "https://api.github.com/users/octocat/events{/privacy}",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": false,
"name": "monalisa octocat",
"company": "GitHub",
"blog": "https://github.com/blog",
"location": "San Francisco",
"email": "octocat@github.com",
"hireable": false,
"bio": "There once was...",
"twitter_username": "monatheoctocat",
"public_repos": 2,
"public_gists": 1,
"followers": 20,
"following": 0,
"created_at": "2008-01-14T04:33:35Z",
"updated_at": "2008-01-14T04:33:35Z",
"private_gists": 81,
"total_private_repos": 100,
"owned_private_repos": 100,
"disk_usage": 10000,
"collaborators": 8,
"two_factor_authentication": true,
"plan": {
"name": "Medium",
"space": 400,
"private_repos": 20,
"collaborators": 0
}
}`

## Get a user using their ID

Provides publicly available information about someone with a GitHub account. This method takes their durable user `ID` instead of their `login`, which can change over time.

If you are requesting information about an [Enterprise Managed User](https://docs.github.com/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-enterprise-managed-users), or a GitHub App bot that is installed in an organization that uses Enterprise Managed Users, your requests must be authenticated as a user or GitHub App that has access to the organization to view that account's information. If you are not authorized, the request will return a `404 Not Found` status.

The `email` key in the following response is the publicly visible email address from your GitHub [profile page](https://github.com/settings/profile). When setting up your profile, you can select a primary email address to be public which provides an email entry for this endpoint. If you do not set a public email address for `email`, then it will have a value of `null`. You only see publicly visible email addresses when authenticated with GitHub. For more information, see [Authentication](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#authentication).

The Emails API enables you to list all of your email addresses, and toggle a primary email to be visible publicly. For more information, see [Emails API](https://docs.github.com/rest/users/emails).

### Fine-grained access tokens for "Get a user using their ID"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get a user using their ID"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| account_idintegerRequiredaccount_id parameter |

### HTTP response status codes for "Get a user using their ID"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a user using their ID"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 200get/user/{account_id}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/user/ACCOUNT_ID`

Default response

-
-

`Status: 200``{
"login": "octocat",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octocat",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"repos_url": "https://api.github.com/users/octocat/repos",
"events_url": "https://api.github.com/users/octocat/events{/privacy}",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": false,
"name": "monalisa octocat",
"company": "GitHub",
"blog": "https://github.com/blog",
"location": "San Francisco",
"email": "octocat@github.com",
"hireable": false,
"bio": "There once was...",
"twitter_username": "monatheoctocat",
"public_repos": 2,
"public_gists": 1,
"followers": 20,
"following": 0,
"created_at": "2008-01-14T04:33:35Z",
"updated_at": "2008-01-14T04:33:35Z"
}`

## List users

Lists all users, in the order that they signed up on GitHub. This list includes personal user accounts and organization accounts.

Note: Pagination is powered exclusively by the `since` parameter. Use the [Link header](https://docs.github.com/rest/guides/using-pagination-in-the-rest-api#using-link-headers) to get the URL for the next page of users.

### Fine-grained access tokens for "List users"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "List users"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| sinceintegerA user ID. Only return users with an ID greater than this ID. |
| per_pageintegerThe number of results per page (max 100). For more information, see "Using pagination in the REST API."Default:30 |

### HTTP response status codes for "List users"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 304 | Not modified |

### Code samples for "List users"

#### Request example

get/users

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users`

Response

-
-

`Status: 200``[
{
"login": "octocat",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octocat",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"repos_url": "https://api.github.com/users/octocat/repos",
"events_url": "https://api.github.com/users/octocat/events{/privacy}",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": false
}
]`

## Get a user

Provides publicly available information about someone with a GitHub account.

If you are requesting information about an [Enterprise Managed User](https://docs.github.com/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-enterprise-managed-users), or a GitHub App bot that is installed in an organization that uses Enterprise Managed Users, your requests must be authenticated as a user or GitHub App that has access to the organization to view that account's information. If you are not authorized, the request will return a `404 Not Found` status.

The `email` key in the following response is the publicly visible email address from your GitHub [profile page](https://github.com/settings/profile). When setting up your profile, you can select a primary email address to be public which provides an email entry for this endpoint. If you do not set a public email address for `email`, then it will have a value of `null`. You only see publicly visible email addresses when authenticated with GitHub. For more information, see [Authentication](https://docs.github.com/rest/guides/getting-started-with-the-rest-api#authentication).

The Emails API enables you to list all of your email addresses, and toggle a primary email to be visible publicly. For more information, see [Emails API](https://docs.github.com/rest/users/emails).

### Fine-grained access tokens for "Get a user"

This endpoint works with the following fine-grained token types :

- [GitHub App user access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-a-user-access-token-for-a-github-app)
- [GitHub App installation access tokens](https://docs.github.com/en/apps/creating-github-apps/authenticating-with-a-github-app/generating-an-installation-access-token-for-a-github-app)
- [Fine-grained personal access tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens#creating-a-fine-grained-personal-access-token)

The fine-grained token does not require any permissions.

This endpoint can be used without authentication if only public resources are requested.

### Parameters for "Get a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

### HTTP response status codes for "Get a user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |

### Code samples for "Get a user"

#### Request examples

Select the example typeExample 1: Status Code 200Example 2: Status Code 200get/users/{username}

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME`

Default response

-
-

`Status: 200``{
"login": "octocat",
"id": 1,
"node_id": "MDQ6VXNlcjE=",
"avatar_url": "https://github.com/images/error/octocat_happy.gif",
"gravatar_id": "",
"url": "https://api.github.com/users/octocat",
"html_url": "https://github.com/octocat",
"followers_url": "https://api.github.com/users/octocat/followers",
"following_url": "https://api.github.com/users/octocat/following{/other_user}",
"gists_url": "https://api.github.com/users/octocat/gists{/gist_id}",
"starred_url": "https://api.github.com/users/octocat/starred{/owner}{/repo}",
"subscriptions_url": "https://api.github.com/users/octocat/subscriptions",
"organizations_url": "https://api.github.com/users/octocat/orgs",
"repos_url": "https://api.github.com/users/octocat/repos",
"events_url": "https://api.github.com/users/octocat/events{/privacy}",
"received_events_url": "https://api.github.com/users/octocat/received_events",
"type": "User",
"site_admin": false,
"name": "monalisa octocat",
"company": "GitHub",
"blog": "https://github.com/blog",
"location": "San Francisco",
"email": "octocat@github.com",
"hireable": false,
"bio": "There once was...",
"twitter_username": "monatheoctocat",
"public_repos": 2,
"public_gists": 1,
"followers": 20,
"following": 0,
"created_at": "2008-01-14T04:33:35Z",
"updated_at": "2008-01-14T04:33:35Z"
}`

## Get contextual information for a user

Provides hovercard information. You can find out more about someone in relation to their pull requests, issues, repositories, and organizations.

The `subject_type` and `subject_id` parameters provide context for the person's hovercard, which returns more information than without the parameters. For example, if you wanted to find out more about `octocat` who owns the `Spoon-Knife` repository, you would use a `subject_type` value of `repository` and a `subject_id` value of `1300192` (the ID of the `Spoon-Knife` repository).

OAuth app tokens and personal access tokens (classic) need the `repo` scope to use this endpoint.

### Fine-grained access tokens for "Get contextual information for a user"

This endpoint does not work with GitHub App user access tokens, GitHub App installation access tokens, or fine-grained personal access tokens.

### Parameters for "Get contextual information for a user"

| Name, Type, Description |
| --- |
| acceptstringSetting toapplication/vnd.github+jsonis recommended. |

| Name, Type, Description |
| --- |
| usernamestringRequiredThe handle for the GitHub user account. |

| Name, Type, Description |
| --- |
| subject_typestringIdentifies which additional information you'd like to receive about the person's hovercard. Can beorganization,repository,issue,pull_request.Requiredwhen usingsubject_id.Can be one of:organization,repository,issue,pull_request |
| subject_idstringUses the ID for thesubject_typeyou specified.Requiredwhen usingsubject_type. |

### HTTP response status codes for "Get contextual information for a user"

| Status code | Description |
| --- | --- |
| 200 | OK |
| 404 | Resource not found |
| 422 | Validation failed, or the endpoint has been spammed. |

### Code samples for "Get contextual information for a user"

#### Request example

get/users/{username}/hovercard

-
-
-

`curl -L \
  -H "Accept: application/vnd.github+json" \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "X-GitHub-Api-Version: 2022-11-28" \
  https://api.github.com/users/USERNAME/hovercard`

Response

-
-

`Status: 200``{
"contexts": [
{
"message": "Owns this repository",
"octicon": "repo"
}
]
}`
