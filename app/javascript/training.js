// ./ant js-utest -Djstest.verbose=true -Djstest.modules= -Djstest.path=../ui-sfdc/test/unit/javascript/training.js

Function.RegisterNamespace('Test.Training')
// ----------------------------
// -------API under test-------
// ----------------------------
var WeatherHelper = function (domElements) {
  var config
  this.parseParams = function (params) {
    config = JSON.parse(this.encodeDecodeParams(params))
  }

  this.encodeDecodeParams = function (params) {
    	return decodeURIComponent(escape(atob(params)))
  }

  this.setTemp = function (weather, isDaytime) {
    var temp
    if (isDaytime) {
      temp = config.weatherConfig.isFahrenheit ? weather.highF : weather.highC
    } else {
      temp = config.weatherConfig.isFahrenheit ? weather.lowF : weather.lowC
    }
    domElements.temp.innerText = temp + '\u00B0'
  }
}

// --------Test Case -----------
// ----Using Mocks and Stubs----
// -----------------------------
[Fixture, ScrumTeam('Sfdc')]
Test.Training.WeatherHelperTests = function () {
  [Fixture]
  function setTemp () {
    [Fact]
    function setsHighFforDaytimeFahrenheit () {
			// Arrange
      var domElements = {}
      var weatherHelper = new WeatherHelper(domElements)
      var atobMock = Mocks.GetMock(Object.Global(), 'atob', function (a) {
        return a
      })
			// Act

			// Assert
      Assert.Equal(1, 2)
    }
  }
}

// https://git.soma.salesforce.com/gist/a-rich/9364be4b6eb2d596e793274935640579
