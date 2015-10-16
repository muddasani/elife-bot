Feature: Generate correct EIF from article JSON
  As a consumer of the article data, I need the correct EIF to be generated from
  upstream article JSON, and deposited correctly, so I can use it appropriately.

  Scenario: Verify a file has been generated in the correct location for EIF files
    Given the reference EIF file elife-07301-v1-eif-reference.json is available
    And the EIF destination location is available
    And I empty the EIF destination location before I start
    When I trigger the generation of the EIF file from the source file elife-00353-vor.zip
    Then I expect to see a file in the EIF destination with the filename elife-07301-v1.json
#    And I expect that the generated file to be functionally identical to the reference file
