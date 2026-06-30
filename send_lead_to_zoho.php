<?php
// === CONFIGURATION SECTION ===

// Replace these with your actual Zoho credentials
$client_id = '';
$client_secret = '';
$refresh_token = '';
$redirect_uri = 'https://flatbuffer.com/mav';
$zoho_domain = 'https://www.zohoapis.com'; // change to .eu, .in if needed

// === STEP 1: Get a new access token from refresh token ===

function getAccessToken($client_id, $client_secret, $refresh_token, $zoho_domain) {
    $url = "https://accounts.zoho.com/oauth/v2/token";
    $data = http_build_query([
        'refresh_token' => $refresh_token,
        'client_id' => $client_id,
        'client_secret' => $client_secret,
        'grant_type' => 'refresh_token'
    ]);

    $options = [
        'http' => [
            'header'  => "Content-type: application/x-www-form-urlencoded",
            'method'  => 'POST',
            'content' => $data
        ]
    ];
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    if ($result === FALSE) {
        die("Error retrieving access token.");
    }

    $response = json_decode($result, true);
    return $response['access_token'];
}

// === STEP 2: Prepare the lead/message data ===

$testMessage = "Hi, I’m Yaw Oh. Reach out.";
$leadData = [
    "data" => [[
        "First_Name" => "Yaw",
        "Last_Name" => "Oh",
        "Phone" => "0200000001",
        "Email" => "yawoh24@example.com",
        "Company" => "GoLive Team",
        "Description" => $testMessage,
        "Lead_Source" => "OpenAI Assistant"
    ]]
];

// === STEP 3: Send lead data to Zoho CRM ===

function sendLeadToZoho($access_token, $leadData, $zoho_domain) {
    $url = $zoho_domain . "/crm/v2/Leads";
    $data_string = json_encode($leadData);

    $headers = [
        "Authorization: Zoho-oauthtoken $access_token",
        "Content-Type: application/json",
        "Content-Length: " . strlen($data_string)
    ];

    $options = [
        'http' => [
            'header'  => implode("\r\n", $headers),
            'method'  => 'POST',
            'content' => $data_string
        ]
    ];
    $context  = stream_context_create($options);
    $result = file_get_contents($url, false, $context);

    if ($result === FALSE) {
        die("Error sending data to Zoho CRM.");
    }

    $response = json_decode($result, true);
    return $response;
}

// === STEP 4: Run the script ===

echo "Getting access token...\n";
$access_token = getAccessToken($client_id, $client_secret, $refresh_token, $zoho_domain);

echo "Sending lead to Zoho CRM...\n";
$response = sendLeadToZoho($access_token, $leadData, $zoho_domain);

echo "Response from Zoho CRM:\n";
print_r($response);

?>
